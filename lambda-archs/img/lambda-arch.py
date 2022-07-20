from turtle import rt
from diagrams import Diagram, Cluster
import diagrams.aws.network as network
import diagrams.aws.compute as compute
import diagrams.aws.storage as storage
import diagrams.aws.security as security
import diagrams.onprem.client as client
import diagrams.firebase.develop as firebase
import diagrams.onprem.container as container
import diagrams.programming.framework as framework

with Diagram("lambda local arch", show=False):
    with Cluster("on_aws"):
        client1 = client.Client("from browser")
        vue_s3 = storage.S3("vue-spa")
        cloudfront = network.CloudFront("CloudFront")
        apigw1 = network.APIGateway("apigw")
        lambda1 = compute.Lambda("lambda")
        client1 >> cloudfront >> vue_s3
        client1 >> cloudfront >> apigw1 >> lambda1
    
    with Cluster("on_local"):
        client_local = client.Client("from browser")

        docker1 = container.Docker("api-gw-mock")
        docker2 = container.Docker("lambda")

        vue_local = framework.Vue("vue-dev-server")
        
        client_local >> vue_local
        client_local >> vue_local >> docker1 >> docker2