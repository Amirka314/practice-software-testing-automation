from pydantic import BaseModel, ConfigDict


class Category(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    name: str
    slug: str


class Brand(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    name: str


class Product(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    name: str
    description: str
    price: float
    is_location_offer: bool
    is_rental: bool
    co2_rating: str
    in_stock: bool
    is_eco_friendly: bool
    category: Category
    brand: Brand


class ProductsPage(BaseModel):
    model_config = ConfigDict(extra="ignore")
    current_page: int
    data: list[Product]
    per_page: int
    last_page: int
    total: int


class LoginResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    access_token: str