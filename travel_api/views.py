import datetime

from django.db.models import F
from django.http import JsonResponse
from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.views.generic import TemplateView, View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from rest_framework import filters, exceptions
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from .utils import *
from .serializers import *
import jwt


class TourPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 10



class TourSiteMapPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 60


class ToursList(generics.ListCreateAPIView):
    serializer_class = TourSerializer
    pagination_class = TourPagination
    ordering_fields = ['name', 'free_places', 'price', 'date_start']
    ordering = ['name', 'free_places']

    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = Tour.objects.all().order_by(*self.ordering)

        seasons = self.request.query_params.getlist('season', [])
        if seasons:
            queryset = queryset.filter(season__name__in=seasons)

        durations = self.request.query_params.getlist('duration', [])
        if durations:
            queryset = Tour.objects.filter(
                date_end__in=[F('date_start') + datetime.timedelta(days=int(dur)) for dur in durations])

        ordering = self.request.query_params.get('ordering', '')
        if ordering:
            try:
                queryset = queryset.order_by(ordering)
            except FieldError:
                raise exceptions.ParseError(detail=f"Unsupported ordering field: {ordering}")

        return queryset


class TourSearch(generics.ListAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    pagination_class = TourPagination

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'free_places', 'price', 'date_start']

    def get_queryset(self):
        queryset = super(TourSearch, self).get_queryset()

        seasons = self.request.query_params.getlist('season', [])
        if seasons:
            queryset = queryset.filter(season__name__in=seasons)

        durations = self.request.query_params.getlist('duration', [])
        if durations:
            for dur in durations:
                end_date = F('date_start') + datetime.timedelta(days=int(dur))
                queryset = queryset.filter(date_end=end_date)

        ordering = self.request.query_params.get('ordering', '')
        if ordering:
            try:
                queryset = queryset.order_by(ordering)
            except FieldError:
                return Response({'error': 'Sorting by incorrect field'})

        return queryset


class FeaturedTours(generics.ListAPIView):
    serializer_class = TourSerializer
    pagination_class = TourPagination

    def get_queryset(self):
        try:
            return get_featured_tours()
        except TimeoutError:
            return Response({'error': 'Request timeout'}, status=503)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class SiteMapTours(generics.ListAPIView):
    queryset = Tour.objects.all().order_by('-id')
    serializer_class = SiteMapSerializer
    pagination_class = TourSiteMapPagination

    def get_queryset(self):
        queryset = super(SiteMapTours, self).get_queryset()
        try:
            return queryset
        except TimeoutError:
            return Response({'error': 'Request timeout'}, status=503)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class DetailsTour(APIView):
    def get(self, request, id):
        try:
            tour = Tour.objects.get(id=id)
            return Response(DetailsSerializer(tour, many=False).data)
        except ObjectDoesNotExist:
            return Response({'error': 'Tour not found'}, status=404)
        except TimeoutError:
            return Response({'error': 'Request timeout'}, status=503)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class OrderDetailsTour(APIView):
    def get(self, request, id):
        try:
            tour = Tour.objects.get(id=id)
            return Response(TourSerializer(tour, many=False).data)
        except ObjectDoesNotExist:
            return Response({'error': 'Tour not found'}, status=404)
        except TimeoutError:
            return Response({'error': 'Request timeout'}, status=503)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class PayView(TemplateView):
    template_name = 'billing/pay.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'signature': request.GET.get('signature'),
            'data': request.GET.get('data')
        })


@method_decorator(csrf_exempt, name='dispatch')
class PayCallbackView(View):
    def post(self, request, *args, **kwargs):
        try:
            response = get_liqpay_decoded_response(request)
            payment_status = get_liqpay_payment_status(response)
        except Exception as e:
            return JsonResponse({'error': 'Attempt to retrieve payment data failed from Liqpay.' + str(e)}, status=500)
        if payment_status.get('status') == "error":
            send_mail_(f"Помилка із замовленням №{response.get('order_id')}",
                       generate_order_bad_request_email(response, payment_status))
            return JsonResponse({'error': payment_status}, status=402)
        try:
            order = update_order(payment_status)
            order_response = get_order_response(order, response)
        except Exception as e:
            send_mail_(f"#ERROR із замовленням №{response.get('order_id')}",
                       generate_order_server_error_email(response, payment_status))
            return JsonResponse({'error': str(e)}, status=500)

        send_mail_("Admin, було успішно сформовано нове замовлення",
                   generate_order_successful_email(order_response, get_passengers_info(order)))
        send_mail_("SMS sending test", generate_sms(order))
        payload = {
            'order_pk': order.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=48)
        }
        return JsonResponse({"token": jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')}, status=200)


class OrderPaymentSuccessfulView(APIView):
    def post(self, request):
        token = request.headers.get('Authorization').split(' ')[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            order_id = payload.get('order_pk')
            if not order_id:
                return Response({"error": "Invalid token. Order is missing in the token."}, status=404)
        except (jwt.ExpiredSignatureError, jwt.DecodeError, ValueError):
            raise PermissionDenied(detail="Invalid or expired token.")

        try:
            order = Order.objects.get(pk=order_id)
        except ObjectDoesNotExist:
            return Response({"error": "Invalid token. Order not found."}, status=404)

        try:
            response_data = get_order_successful_response(order)
        except Exception as e:
            return Response({"error": f"Can not get response info. {e}"}, status=500)

        return Response(response_data, status=200)


class OrderPaymentView(APIView):
    def post(self, request, tour_id):
        try:
            request.data['tour_id'] = tour_id
            tour = Tour.objects.get(id=request.data['tour_id'])
        except ObjectDoesNotExist:
            return Response({'error': 'Tour not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

        if not request.data.get('passengers') or len(request.data.get('passengers')) < 1:
            return JsonResponse({'error': 'Number of passengers must be more than 1'}, status=400)

        if not check_tour_has_available_places(tour, request):
            return JsonResponse({'error': 'Not enough available places in this tour for your order'}, status=400)

        if not check_order_cost(tour, request):
            return JsonResponse({'error': 'You are trying to pay with incorrect cost'}, status=400)

        try:
            order = create_new_order(tour, request)
            create_order_items(request, order, tour)
        except Exception as e:
            return JsonResponse({'error': 'Failed Order creation in DB. ' + str(e)}, status=500)

        try:
            response_data = get_order_successful_response(order)
            tour = Tour.objects.get(pk=order.tour.pk)
            send_mail_("Admin, було успішно сформовано нове замовлення",
                       generate_temporary_order_successful_email(order, tour, get_passengers_info(order)))
        except Exception as e:
            return Response({"error": f"Can not get response info. {e}"}, status=500)

        return Response(response_data, status=200)


class CheckOrderCodeView(APIView):
    def post(self, request, order_code):
        try:
            code = request.data.get('code')
        except Exception as e:
            return Response({'error': 'Can not get code. ' + str(e)}, status=500)
        try:
            order = Order.objects.get(code=order_code)
        except ObjectDoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        verification_code = get_user_code(order)
        if not verification_code:
            return Response({"error": "Can not get verification code."}, status=500)

        if verification_code != code:
            return Response({"error": "Invalid verification code."}, status=400)

        payload = {
            'order_code': order.code,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        return Response({"token": jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')}, status=200)


class ClientOrderInfoView(APIView):

    def get(self, request):
        token = request.headers.get('Authorization').split(' ')[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            order_code = payload.get('order_code')
            if not order_code:
                return Response({"error": "Invalid token. Order code is missing in the token."}, status=404)
        except (jwt.ExpiredSignatureError, jwt.DecodeError, ValueError):
            raise PermissionDenied(detail="Invalid or expired token.")

        try:
            order = Order.objects.get(code=order_code)
        except ObjectDoesNotExist:
            return Response({"error": "Invalid token. Order not found."}, status=404)

        try:
            response_data = get_client_order_response(order)
        except Exception as e:
            return Response({"error": f"Can not get response info. {e}"}, status=500)

        return Response(response_data, status=200)
