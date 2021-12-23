'''Sample logic for API'''
from django.utils.translation import ugettext as _

from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from common.helper import get_languages_array

from .serializers import SampleNonGenericSerializer


class SampleView(viewsets.ViewSet):
    '''API view for Sample'''
    lookup_field = 'sample_id'

    # pylint: disable=no-self-use
    def list(self, request: Request) -> Response:
        '''
        GET /sample
        List all samples
        '''
        # If the language is not in the handled languages, we set it as default
        lang = request.META.get('HTTP_ACCEPT_LANGUAGE')
        if lang not in get_languages_array():
            lang = 'en'
        return Response({'message': _('Success')}, status=status.HTTP_200_OK)


    # pylint: disable=invalid-name, no-self-use
    def retrieve(self, request: Request, sample_id: str = None) -> Response:
        '''
        GET /sample/<sample_id>
        Retrieve a specific sample
        '''
        # If the language is not in the handled languages, we set it as default
        lang = request.META.get('HTTP_ACCEPT_LANGUAGE')
        if lang not in get_languages_array():
            lang = 'en'
        return Response({'message': _('Success')}, status=status.HTTP_200_OK)


    # pylint: disable=no-self-use
    def create(self, request: Request) -> Response:
        '''
        POST /sample
        Create a sample
        '''
        # If the language is not in the handled languages, we set it as default
        lang = request.META.get('HTTP_ACCEPT_LANGUAGE')
        if lang not in get_languages_array():
            lang = 'en'
        return Response({'message': _('Success')}, status=status.HTTP_201_CREATED)


    # pylint: disable=invalid-name, no-self-use
    def update(self, request: Request, sample_id: str = None) -> Response:
        '''
        PUT /sample/<sample_id>
        Update a sample
        '''
        # If the language is not in the handled languages, we set it as default
        lang = request.META.get('HTTP_ACCEPT_LANGUAGE')
        if lang not in get_languages_array():
            lang = 'en'
        return Response({'message': _('Success')}, status=status.HTTP_200_OK)


    # pylint: disable=invalid-name, no-self-use
    def destroy(self, request: Request, sample_id: str = None) -> Response:
        '''
        DELETE /sample/<sample_id>
        Delete a sample
        '''
        # If the language is not in the handled languages, we set it as default
        lang = request.META.get('HTTP_ACCEPT_LANGUAGE')
        if lang not in get_languages_array():
            lang = 'en'
        return Response({'message': _('Success')}, status=status.HTTP_200_OK)


    # pylint: disable=no-self-use
    def post_sample_non_generic(self, request: Request) -> Response:
        '''
        POST /sample/non-generic
        Sample non generic view
        '''
        # If the language is not in the handled languages, we set it as default
        lang = request.META.get('HTTP_ACCEPT_LANGUAGE')
        if lang not in get_languages_array():
            lang = 'en'

        # Check the data validity
        serializer = SampleNonGenericSerializer(data=request.data)
        if serializer.is_valid() is False:
            return Response({'message': _('Error')}, status=status.HTTP_400_BAD_REQUEST)

        # Get the data from serializer
        data = serializer.validated_data
        return Response({'message': _('Success')}, status=status.HTTP_200_OK)
