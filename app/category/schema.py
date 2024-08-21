from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryInDb(CategoryBase):
    id: int

    class Config:
        orm_mode = True