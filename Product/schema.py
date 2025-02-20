from cmath import pi
from dataclasses import field
import re
import graphene
from graphene_django import DjangoObjectType
from .models import Categorie, Picture, Produit, Produit_Image 
from graphene_file_upload.scalars import Upload
class CategorieType(DjangoObjectType):
    class Meta:
        model = Categorie 
        fields = ("id" , "name" , "slug")

class AddCategorieMutation(graphene.Mutation):
    class Arguments : 
        name = graphene.String(required = True)
        slug = graphene.String(required = True) 
    
    categorie = graphene.Field(CategorieType)
    @classmethod
    def mutate(cls , root , info , name , slug):
        categorie = Categorie(name = name , slug = slug)
        categorie.save() 
        return AddCategorieMutation(categorie = categorie)


class UpdateCategorieMutation(graphene.Mutation):
    class Arguments : 
        name = graphene.String(required = True)
        slug = graphene.String(required = True)
        id = graphene.Int(required = True)

    categorie = graphene.Field(CategorieType)
    @classmethod
    def mutate(cls , root , info , id ,name , slug):
        categorie = Categorie.objects.get(id = id) 
        categorie.name = name 
        categorie.slug = slug 
        categorie.save() 
        return UpdateCategorieMutation(categorie = categorie)

class DeleteCategorieMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required = True)
    categorie = graphene.Field(CategorieType)
    @classmethod
    def mutate(cls , root , info , id):
        categorie = Categorie.objects.get(id = id)
        categorie.delete() 
        return
# PRODUCT QUERYS AND MUTATIONS AND OBJECT TYPE HEREE
class ProduitType(DjangoObjectType):
    class Meta: 
        model = Produit
        fields = ("id", "name" ,"image", "prix" , "qte" , "categorie")

class ProduitImageType(DjangoObjectType):
    class Meta:
        model = Produit_Image

class PictureType(DjangoObjectType):
    class Meta:
        model = Picture
class ProductImageInput(graphene.InputObjectType):
    image_id = graphene.ID(required=True)

class PictureInput(graphene.InputObjectType):
    image_id = graphene.ID(required = True)


class AddPictureMutation(graphene.Mutation):
    class Arguements : 
        images = Upload(required = True)
    picture = graphene.Field(PictureType)
    @classmethod
    def mutate(self , info , image):
        picture = Picture.objects.create(image = image)
        return AddPictureMutation(images = picture)

        
class AddProduitMutation(graphene.Mutation):
    class Arguments : 
        name = graphene.String(required = True)
        prix = graphene.Int(required = True)
        qte = graphene.Int(required = True) 
        images = graphene.List(ProductImageInput)
        categorie = graphene.Int(required = True)
    produit = graphene.Field(ProduitType)
    @classmethod
    def mutate(self , info , name , prix ,  qte , images , categorie):
        cat = Categorie.objects.get (id = categorie)
        produit = Produit(name = name , prix = prix , qte = qte , categorie = cat) 
        file_data = {}
        '''if image:
            file_data = {"image": image}####'''
        '''produit.image = file_data'''
        produit.save() 
        Produit_Image.objects.bulk_create([
            Produit_Image(product_id=produit.id, **image_data) for image_data in images
        ])

        return AddProduitMutation(produit = produit)

class Query(graphene.ObjectType):
    all_categories = graphene.List(CategorieType)
    def resolve_all_categories(root , info):
        return Categorie.objects.all() 
    categorieByID = graphene.Field(CategorieType , id = graphene.Int())
    def resolve_categorieByID(root , info ,id):
        return Categorie.objects.get(pk = id)
    all_produits = graphene.List(ProduitType) 
    def resolve_all_produits(root , info):
        return Produit.objects.all()
    all_images = graphene.List(PictureType)
    def resolve_all_images(root , info):
        return Picture.objects.all() 

class Mutation(graphene.ObjectType):
    add_categorie = AddCategorieMutation.Field() 
    update_categorie = UpdateCategorieMutation.Field()
    delete_categorie = DeleteCategorieMutation.Field() 
    add_produit = AddProduitMutation.Field()
    addPicture = AddPictureMutation.Field()
schema = graphene.Schema(query = Query , mutation = Mutation)