docker run -it -dp 8040:8040 --name main-api \
    -v $(pwd)/main.env:/dashapp/main.env \
    main-api:latest