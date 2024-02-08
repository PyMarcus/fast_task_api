if __name__ == '__main__':
    from fastapi import FastAPI

    app: FastAPI = FastAPI(
        title="Get users and tasks!",
        description="An API to recover users and yours tasks!")

    app.add_route()
    app.add_route()
    