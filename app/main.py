from fastapi import FastAPI, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .database import get_db, engine
from . import models, schemas


models.Base.metadata.create_all(bind=engine)

app = FastAPI()



@app.get("/")
async def root():
    return "Hello World!"



@app.get("/posts", response_model=list[schemas.Post])
async def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts



@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    return new_post



@app.get("/posts/{id}", response_model=schemas.Post)
async def get_post_by_id(id: int, db: Session = Depends(get_db)):
    post =db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found!")
    return post



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def get_post_by_id(id: int, db: Session = Depends(get_db)):
    post =db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found!")
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}", response_model=schemas.Post)
async def get_post_by_id(id: int, updated_post: schemas.PostBase,db: Session = Depends(get_db)):
    post_query =db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found!")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()
