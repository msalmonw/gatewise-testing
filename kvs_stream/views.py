from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import boto3

def get_hls_url(stream_name):
    client = boto3.client('kinesisvideo')

    response = client.get_data_endpoint(
        StreamName=stream_name,
        APIName='GET_HLS_STREAMING_SESSION_URL')

    kvam_client = boto3.client("kinesis-video-archived-media", endpoint_url=response['DataEndpoint'])
    url = kvam_client.get_hls_streaming_session_url(
    StreamName='gatewise-camera-01',
    PlaybackMode="LIVE"
    )['HLSStreamingSessionURL']
    return url


def kvs(request):
    url = get_hls_url('gatewise-camera-01')
    context = {
        'hls_url': url
    }
    return render(request, 'kvs_stream/test_temp.html', context)
