from aws_cdk import (
    Stack,
    aws_apigateway as apigateway,
    aws_lambda as _lambda,
    aws_iam as iam, Duration,
    aws_dynamodb as dynamodb,
    aws_s3 as s3, RemovalPolicy,
    aws_cognito as cognito,
    aws_sns as sns,
    aws_s3_deployment as s3_deployment,
)
#import aws_cdk as core
from constructs import Construct

class CloudProjekatStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(
            self, "ContentBucket-New2",
            bucket_name="cloud-movies-cdk",

            cors=[
                s3.CorsRule(
                    allowed_methods=[
                        s3.HttpMethods.GET,
                        s3.HttpMethods.PUT,
                        s3.HttpMethods.POST,
                        s3.HttpMethods.DELETE,
                        s3.HttpMethods.HEAD
                    ],
                    allowed_origins=["*"],
                    allowed_headers=["*"]
                )
            ],
            removal_policy=RemovalPolicy.DESTROY
        )
        s3_deployment.BucketDeployment(self, "MoviesFolderCDK",
                                       sources=[s3_deployment.Source.data("movies/", "")],
                                       destination_bucket=bucket,
                                       destination_key_prefix="movies/"
                                       )
        s3_role = iam.Role(
            self, "S3AccessRoleCDK",
            role_name="S3AccessRoleCDK",
            assumed_by=iam.ServicePrincipal("s3.amazonaws.com")  # Postavljamo uslugu koja može koristiti ovu ulogu
        )
        s3_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "s3:GetObject",
                    "s3:PutObject",
                ],
                resources=[
                    "arn:aws:s3:::test-bucket2307/*"
                ]
            )
        )
        topic = sns.Topic(self, "CloudMoviesCDK",
                          display_name="CloudMoviesCDK",
                          topic_name="CloudMoviesCDK")

        actions_sns = [
            "sns:Publish"
        ]

        topic.add_to_resource_policy(
            statement=iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=actions_sns,
                principals=[iam.ServicePrincipal("lambda.amazonaws.com")],
                resources=[topic.topic_arn]
            )
        )
        user_pool = cognito.UserPool(
            self, "CloudMoviesPoolCDK",
            user_pool_name="CloudMoviesPoolCDK",
            self_sign_up_enabled=True,
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            password_policy=cognito.PasswordPolicy(
                min_length=6,
                require_digits=False,
                require_lowercase=False,
                require_uppercase=False,
                require_symbols=False

            ),
            sign_in_aliases=cognito.SignInAliases(username=True),
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(required=True),
                birthdate=cognito.StandardAttribute(required=True),
                given_name=cognito.StandardAttribute(required=True),
                family_name=cognito.StandardAttribute(required=True)
            )
        )
        user_pool_domain = cognito.UserPoolDomain(self, "DomainCDK",
                                                  user_pool=user_pool,
                                                  cognito_domain=cognito.CognitoDomainOptions(
                                                      domain_prefix="kinoteka-cdk"
                                                  )
                                                  )
        client = cognito.UserPoolClient(
            self, "CloudMoviesAppCDK",
            user_pool=user_pool,
            auth_flows=cognito.AuthFlow(
                user_srp=True
            ),
            o_auth={
                'flows': {
                    'implicit_code_grant': True,
                    'authorization_code_grant': True
                },
                'callback_urls': [
                   'http://localhost:4200/auth'
                ],
            },
            generate_secret=False,
            supported_identity_providers=[
                cognito.UserPoolClientIdentityProvider.COGNITO
            ]
        )
        table_movies = dynamodb.Table(
            self, 'MoviesCDK',
            table_name='MoviesCDK',
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            )
        )
        table_movies.add_global_secondary_index(
            index_name="description-index",
            partition_key=dynamodb.Attribute(name="description", type=dynamodb.AttributeType.STRING),
        )
        table_movies.add_global_secondary_index(
            index_name="director-index",
            partition_key=dynamodb.Attribute(name="director", type=dynamodb.AttributeType.STRING),
        )
        table_movies.add_global_secondary_index(
            index_name="title-index",
            partition_key=dynamodb.Attribute(name="title", type=dynamodb.AttributeType.STRING),
        )
        table_actors = dynamodb.Table(
            self, 'ActorsCDK',
            table_name='ActorsCDK',
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            )
        )
        table_actors.add_global_secondary_index(
            index_name="name-index",
            partition_key=dynamodb.Attribute(name="name", type=dynamodb.AttributeType.STRING),
        )
        table_genres = dynamodb.Table(
            self, 'GenresCDK',
            table_name='GenresCDK',
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            )
        )
        table_genres.add_global_secondary_index(
            index_name="name-index",
            partition_key=dynamodb.Attribute(name="name", type=dynamodb.AttributeType.STRING),
        )
        table_subscriptions = dynamodb.Table(
            self, 'SubscriptionsCDK',
            table_name='SubscriptionsCDK',
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            )
        )
        table_subscriptions.add_global_secondary_index(
            index_name="subscription-index",
            partition_key=dynamodb.Attribute(name="subscription", type=dynamodb.AttributeType.STRING),
        )
        table_subscriptions.add_global_secondary_index(
            index_name="username-index",
            partition_key=dynamodb.Attribute(name="username", type=dynamodb.AttributeType.STRING),
        )
        lambda_role = iam.Role(
            self, "LambdaRoleCDK",
            role_name="LambdaRoleCDK",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )
        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
        )
        table_downloads = dynamodb.Table(
            self, 'DownloadsCDK',
            table_name='DownloadsCDK',
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            )
        )
        table_downloads.add_global_secondary_index(
            index_name="username-index",
            partition_key=dynamodb.Attribute(name="username", type=dynamodb.AttributeType.STRING),
        )
        table_ratings = dynamodb.Table(
            self, 'RatingsCDK',
            table_name='RatingsCDK',
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            )
        )
        table_ratings.add_global_secondary_index(
            index_name="username-index",
            partition_key=dynamodb.Attribute(name="username", type=dynamodb.AttributeType.STRING),
        )
        lambda_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "dynamodb:DescribeTable",
                    "dynamodb:Query",
                    "dynamodb:Scan",
                    "dynamodb:GetItem",
                    "dynamodb:PutItem",
                    "dynamodb:UpdateItem",
                    "dynamodb:DeleteItem",
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:PutObjectACL",
                    "cognito-idp:AdminCreateUser",
                    "cognito-idp:AdminInitiateAuth",
                    "cognito-idp:AdminRespondToAuthChallenge",
                    "sns:Publish",
                    "states:StartExecution",
                    "states:DescribeExecution"
                ],
                resources=[
                    f"{bucket.bucket_arn}/*",
                    table_movies.table_arn,
                    table_actors.table_arn,
                    table_genres.table_arn,
                    table_subscriptions.table_arn,
                    table_ratings.table_arn,
                    table_downloads.table_arn,
                    "arn:aws:dynamodb:eu-central-1:211125485950:table/SubscriptionsCDK/index/username-index"
                ]
            )
        )
        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess")
        )
        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
        )
        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSNSFullAccess")
        )
        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonCognitoReadOnly")
        )
        delete_subscription = _lambda.Function(
            self,
            "deleteSubscription",
            function_name="deleteSubscriptionCDK",
            runtime=_lambda.Runtime.PYTHON_3_9,
            layers=[],
            handler="deleteSubscription.lambda_handler",
            code=_lambda.Code.from_asset("DeleteSubscription"),
            memory_size=128,
            timeout=Duration.seconds(10),
            role=lambda_role
        )
        get_subscriptions = _lambda.Function(
            self,
            "getSubscriptions",
            function_name="getSubscriptionsCDK",
            runtime=_lambda.Runtime.PYTHON_3_9,
            layers=[],
            handler="getSubscriptions.lambda_handler",
            code=_lambda.Code.from_asset("GetSubscriptions"),
            memory_size=128,
            timeout=Duration.seconds(10),
            role=lambda_role
        )
        personalized_feed = _lambda.Function(
            self,
            "personalizedFeed",
            function_name="personalizedFeedCDK",
            runtime=_lambda.Runtime.PYTHON_3_9,
            layers=[],
            handler="personalizedFeed.lambda_handler",
            code=_lambda.Code.from_asset("PersonalizedFeed"),
            memory_size=128,
            timeout=Duration.seconds(10),
            role=lambda_role
        )
        add_rating = _lambda.Function(
            self,
            "addRating",
            function_name="addRatingCDK",
            runtime=_lambda.Runtime.PYTHON_3_9,
            layers=[],
            handler="addRating.lambda_handler",
            code=_lambda.Code.from_asset("AddRating"),
            memory_size=128,
            timeout=Duration.seconds(10),
            role=lambda_role
        )
        add_movie = _lambda.Function(
            self,
            "addMovie",
            function_name="addMovieCDK",
            runtime=_lambda.Runtime.PYTHON_3_9,
            layers=[],
            handler="addMovie.lambda_handler",
            code=_lambda.Code.from_asset("AddMovie"),
            memory_size=128,
            timeout=Duration.seconds(10),
            role=lambda_role
        )
        delete_movie = _lambda.Function(
            self,
            "deleteMovie",
            function_name="deleteMovieCDK",
            runtime=_lambda.Runtime.PYTHON_3_9,
            layers=[],
            handler="deleteMovie.lambda_handler",
            code=_lambda.Code.from_asset("DeleteMovie"),
            memory_size=128,
            timeout=Duration.seconds(10),
            role=lambda_role
        )
        download_movie = _lambda.Function(
            self,
            "downloadMovie",
            function_name="downloadMovieCDK",
            runtime=_lambda.Runtime.PYTHON_3_9,
            layers=[],
            handler="downloadMovie.lambda_handler",
            code=_lambda.Code.from_asset("DownloadMovie"),
            memory_size=128,
            timeout=Duration.seconds(10),
            role=lambda_role
        )
        get_all_movies = _lambda.Function(
            self,
            "getAllMovies",
            function_name="getAllMoviesCDK",
            runtime=_lambda.Runtime.PYTHON_3_9,
            layers=[],
            handler="getAllMovies.lambda_handler",
            code=_lambda.Code.from_asset("GetAllMovies"),
            memory_size=128,
            timeout=Duration.seconds(10),
            role=lambda_role
        )
        get_movie = _lambda.Function(
            self,
            "getMovie",
            function_name="getMovieCDK",
            runtime=_lambda.Runtime.PYTHON_3_9,
            layers=[],
            handler="getMovie.lambda_handler",
            code=_lambda.Code.from_asset("GetMovie"),
            memory_size=128,
            timeout=Duration.seconds(10),
            role=lambda_role
        )
        search_movie = _lambda.Function(
            self,
            "searchMovie",
            function_name="searchMovieCDK",
            runtime=_lambda.Runtime.PYTHON_3_9,
            layers=[],
            handler="searchMovie.lambda_handler",
            code=_lambda.Code.from_asset("SearchMovie"),
            memory_size=128,
            timeout=Duration.seconds(10),
            role=lambda_role
        )
        subscribe = _lambda.Function(
            self,
            "subscribe",
            function_name="subscribeCDK",
            runtime=_lambda.Runtime.PYTHON_3_9,
            layers=[],
            handler="subscribe.lambda_handler",
            code=_lambda.Code.from_asset("Subscribe"),
            memory_size=128,
            timeout=Duration.seconds(10),
            role=lambda_role
        )
        api_gateway_role = iam.Role(self, "ApiGatewayRoleCDK",
                                    role_name="ApiGatewayRoleCDK",
                                    assumed_by=iam.ServicePrincipal("apigateway.amazonaws.com"),
                                    description="Role for API Gateway to invoke lambda functions")

        api_gateway_role.add_to_policy(iam.PolicyStatement(
            actions=["lambda:InvokeFunction"],
            resources=["*"]  # mogu ovde stativi specificirane lambde
        ))
        self.api = apigateway.RestApi(self, "CloudMoviesApiCDK",
                                      rest_api_name="CloudMoviesApiCDK",
                                      endpoint_types=[apigateway.EndpointType.REGIONAL],
                                      default_cors_preflight_options={
                                          "allow_origins": apigateway.Cors.ALL_ORIGINS,
                                          "allow_methods": apigateway.Cors.ALL_METHODS
                                      },
                                      )
        movies_resource = self.api.root.add_resource("movies")
        movies_resource.add_method("GET", apigateway.LambdaIntegration(get_all_movies, credentials_role=api_gateway_role, proxy=True))
        movies_resource.add_method("POST", apigateway.LambdaIntegration(add_movie, credentials_role=api_gateway_role, proxy=True))
        movies_resource_feed = movies_resource.add_resource("feed")
        movies_resource_feed.add_method("GET", apigateway.LambdaIntegration(personalized_feed, credentials_role=api_gateway_role, proxy=True))
        movies_resource_rate = movies_resource.add_resource("rate")
        movies_resource_rate_title = movies_resource_rate.add_resource("{title}")
        movies_resource_rate_title.add_method("POST", apigateway.LambdaIntegration(add_rating, credentials_role=api_gateway_role, proxy=True))
        movies_resource_title = movies_resource.add_resource("{title}")
        movies_resource_title.add_method("DELETE", apigateway.LambdaIntegration(delete_movie, credentials_role=api_gateway_role, proxy=True))
        movies_resource_title.add_method("GET", apigateway.LambdaIntegration(get_movie, credentials_role=api_gateway_role, proxy=True))
        movies_resource_download = movies_resource.add_resource("download")
        movies_resource_download_title = movies_resource_download.add_resource("{title}")
        movies_resource_download_title.add_method("GET", apigateway.LambdaIntegration(download_movie, credentials_role=api_gateway_role, proxy=True))
        movies_resource_search = movies_resource.add_resource("search")
        movies_resource_search.add_method("POST", apigateway.LambdaIntegration(search_movie, credentials_role=api_gateway_role, proxy=True))

        subscribe_resource = self.api.root.add_resource("subscribe")
        subscribe_resource.add_method("POST", apigateway.LambdaIntegration(subscribe, credentials_role=api_gateway_role, proxy=True))
        subscribe_resource.add_method("GET", apigateway.LambdaIntegration(get_subscriptions, credentials_role=api_gateway_role,
                                                                           proxy=True))
        subscribe_resource.add_method("DELETE", apigateway.LambdaIntegration(delete_subscription, credentials_role=api_gateway_role,
                                                                           proxy=True))
        api_deployment = apigateway.Deployment(self, "ApiDeploymentCDK",
                                                   api=self.api)

        # novi stage
        apigateway.Stage(self, "stageCDK",
                         deployment=api_deployment,
                         stage_name="noviStage")