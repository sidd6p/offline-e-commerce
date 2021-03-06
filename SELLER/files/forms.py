from flask_wtf import FlaskForm

from files.models import Seller

from flask_wtf.file import  (
                            FileField,
                            FileAllowed
                            )

from wtforms import     (
                        StringField, 
                        SubmitField,    
                        BooleanField, 
                        IntegerField, 
                        TextAreaField, 
                        PasswordField, 
                        EmailField
                        )

from wtforms.validators import  (
                                Length, 
                                DataRequired, 
                                Email, 
                                EqualTo, 
                                NumberRange, 
                                ValidationError
                                )



class ShopAccount(FlaskForm):
    sellerFirstName = StringField("First Name", validators = [DataRequired(), Length(min = 1, max = 50, message = "Field length shoud be bewteen 1 to 50 characters")])
    sellerLastName = StringField("Last Name", validators = [DataRequired(), Length(min = 1, max = 50, message = "Field length shoud be bewteen 1 to 50 characters")])
    email = EmailField("Email", validators = [DataRequired(message = "This field is required"), Email(message = "Provide a valid Email-Id")])
    pswd = PasswordField("Password", validators = [DataRequired(message = "This field is required"), Length(min = 8, message = "Minimum Length should be 8")])
    confirmPswd = PasswordField("Confirm Password", validators = [DataRequired(message = "This field is required"), EqualTo('pswd', message = "Password did not match!")])
    shopName = StringField("Title of your shop", validators = [DataRequired(), Length(min = 5, max = 50, message = "Field length shoud be bewteen  5 to 50 characte")])
    shopLogo = FileField("Shop Logo/Picture", validators = [DataRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'png'], message = "Allowed file type are: 'jpg', 'png', 'jpeg', 'png'")])
    address = TextAreaField("Address/Locality", validators = [DataRequired(), Length(min = 5, max = 500, message = "Field length shoud be bewteen  5 to 500 characte")])
    city = StringField("City", validators = [DataRequired(), Length(min = 1, max = 50, message = "Field length shoud be bewteen 1 to 50 characte")])
    state = StringField("State", validators = [DataRequired(), Length(min = 1, max = 50, message = "Field length shoud be bewteen 1 to 50 characte")])
    pin = IntegerField("PIN", validators = [DataRequired(), NumberRange(min = 000000, max = 999999)])
    submit = SubmitField("Create Shop")
    
    def validate_email(self, email):
        hasSeller = Seller.query.filter_by(email=email.data).first()
        if hasSeller:
            raise ValidationError('That email is taken. Please choose a different one.')


class UploadProduct(FlaskForm):
    productName = StringField("Product Name", validators = [DataRequired(), Length(min = 5, max = 50, message = "Product Name length should be between 5 to 50 characters")])
    productType = StringField("Product Type", validators = [DataRequired(), Length(min = 5, max = 100, message = "Product Type length should be between 5 to 100 characters")])
    productPhoto = FileField("Product Picture", validators = [DataRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'png'], message = "Allowed file type are: 'jpg', 'png', 'jpeg', 'png'")])
    productDesc = TextAreaField("Product Description", validators = [DataRequired(), Length(min = 5, max = 500, message = "Product Name length should be between 5 to 500 characters")])
    productPrice = IntegerField("Product Price", validators = [DataRequired()])
    submit = SubmitField("Upload Product")


class Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')
