from fastapi import APIRouter, status, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from .. import schemas, models, database, utils

router = APIRouter(
    prefix="/user",
    tags=["USERS"]
)

@router.get("/", response_model=list[schemas.UserOut])
async def get_all_user(db: Session = Depends(database.get_db)):
    
    users = db.query(models.User).all()
    
    return users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    
    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
async def get_user_by_id(id: int, db: Session = Depends(database.get_db)):
    
    user =db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} was not found!")
    
    return user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(id: int, db: Session = Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} was not found!")
    user.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)