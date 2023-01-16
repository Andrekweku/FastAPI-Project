from fastapi import FastAPI

# from . import models
# from .database import engine
from .routers import post, user, auth, vote

# from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine) -- alembic has replaced this

app = FastAPI(title = "Social Media API", description= "Social Media API with feature to Vote on Posts")

origins = ["*"]  # ["https://www.google.com"] #only domains you want access to your API

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


# while True:

#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="19hrs - Tutorial",
#             user="postgres",
#             password="GOOGLE4LYF",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("Database connection was successful.")
#         break
#     except Exception as error:
#         print("Connecting to Database failed")
#         print("Error: ", error)
#         time.sleep(2)

# my_posts = [
#     {"title": "title of post 1", "content": "content of post 1", "id": 1},
#     {"title": "favorite foods", "content": "I love Pizza", "id": 2},
# ]


# @app.get("/sqlalchemy")
# def test_post(db: Session = Depends(get_db)):

#     posts = db.query(models.Post).all()
#     # print(posts)
#     return {"data": posts}
