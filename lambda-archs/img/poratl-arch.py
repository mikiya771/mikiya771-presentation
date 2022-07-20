from turtle import rt
from diagrams import Diagram, Cluster
import diagrams.aws.network as network
import diagrams.aws.compute as compute
import diagrams.aws.storage as storage
import diagrams.aws.security as security
import diagrams.onprem.client as client
import diagrams.firebase.develop as firebase

with Diagram("Web Service", show=False):
    client1 = client.Client("from browser")
    
    cloudfront = network.CloudFront("CloudFront")
    client1 >> cloudfront

    s3 = storage.S3("SPA Resource")

    with Cluster("R-ISUCON"):
        bench = compute.EC2("bench marker")

        with Cluster("competitors"):
            with Cluster("teamA"):
                c1a= compute.EC2("")
                c2a=compute.EC2("")
                c3a=compute.EC2("")
                c1a-c2a-c3a
            with Cluster("teamB"):
                c1b = compute.EC2("")
                c2b = compute.EC2("")
                c3b = compute.EC2("")
                c1b-c2b-c3b
            bench >> c1a



    with Cluster("backend cluster"):
        apigw1 = network.APIGateway("apigw")
        lambda_count = 2
        ecr_list = [ compute.ECR("repo {}".format(x)) for x in range(lambda_count) ]
        lambda_list = [ compute.Lambda("function {}".format(x)) for x in range(lambda_count)]
        for i in range(lambda_count):
            lambda_list[i] << ecr_list[i] 
        cloudfront >> s3
        cloudfront >> apigw1
        for i in lambda_list:
            apigw1 >> i

    with Cluster("firebase"):
        auth = firebase.Authentication("auth")
        rtdb = firebase.RealtimeDatabase("realtime databse")
        client1 >> auth
        client1 >> rtdb
        rtdb << bench
    
    for i in lambda_list:
        rtdb << i
        auth << i
    
