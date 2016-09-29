django-sorl-cropping
=====================

``django-sorl-cropping`` is an app for cropping uploaded images via Django's admin backend using `Jcrop 
<https://github.com/tapmodo/Jcrop>`_. It keeps the original image intact, only cropping when the image
is being displayed. Large images are presented in a small format, so even very big images can easily be cropped.

``django-sorl-cropping`` is perfect when you need images with a specific size for your templates but want your
users or editors to upload images of any dimension. It presents a selection with a fixed aspect ratio so your users
can't break the layout with oddly-sized images.

It provides the necessary fields, widgets and a (`sorl.thumbnail 
<https://github.com/sorl/sorl-thumbnail>`_) thumbnail processor for displaying the 
cropped image in your templates.

Screenshot: 

.. image:: http://www.jonasundderwolf.de/media/images/django_image_cropping_example.png

Installation
------------

#. Install django-sorl-cropping using pip. For example::

    pip install git+git://github.com/NElias/django-sorl-cropping.git

#. Add ``sorl.thumbnail`` and ``image_cropping`` to your INSTALLED_APPS. ``image_cropping`` is only required
   if you are using Django 1.3+ and ``contrib.staticfiles`` or want to use the ``image_cropping`` templatetag.

#. Adjust the thumbnail engine for ``sorl.thumbnail`` in your ``settings.py``::

    THUMBNAIL_ENGINE = 'sorl_cropping.engine.CropEngine'


Configuration
-------------

To your model containing an ImageField, add an ``ImageRatioField``, which will contain the boundaries
of the cropped image. The ``ImageRatioField`` expects the name of the associated ImageCropField as the
first argument and the size of the final image to be displayed as the second argument.

The size is passed in as a string and defines the aspect ratio of the selection as well as the minimum
size for the final image. You can configure a warning if users try to crop a selection smaller than this
size (see below).

1. Model fields and options::

    from django.db import models
    from sorl_cropping import ImageRatioField

    class MyModel(models.Model):
        image = models.ImageField(blank=True, null=True, upload_to='uploaded_images')
        # size is "width x height"
        cropping = ImageRatioField('image', '430x360')

2. In your admin class, add the ImageCroppingMixin in order to see the cropping widget::

    from django.contrib import admin
    from sorl_cropping import ImageCroppingMixin

    class MyModelAdmin(ImageCroppingMixin, admin.ModelAdmin):
        pass
    admin.site.register(MyModel, MyModelAdmin)

   If your setup is correct you should now see the enhanced image widget that provides a selection
   area for the image in the admin backend. 

3. Additionally, you can define the maximum size of the preview thumbnail in the admin in your ``settings.py``::

    # size is "width x height"
    SORL_CROPPING_THUMB_SIZE = (300, 300)

4. You can warn users about crop selections that are smaller than the size defined in the ImageRatioField.
   When users try to do a smaller selection, a red border appears around the image. To use this functionality,
   add the parameter to the ImageRatioField::

    cropping = ImageRatioField('image', '430x360', size_warning=True)

   You can enable this functionality project-wide by adding the following line to your ``settings.py``::

    SORL_CROPPING_SIZE_WARNING = True


Frontend
--------

You can also use the standard ``sorl.thumbnail`` templatetag with the "crop" parameter::

    {% load thumbnails %}
    {% thumbnail yourmodel.image '430x360' crop=yourmodel.cropping as im %}
        <img src="{{ im.url }}" width="{{ im.width }}" height="{{ im.height }}">
    {% endthumbnail %}

Or generate the URL from Python code in your view::

    from sorl.thumbnail import get_thumbnail
    thumbnail_url = get_thumbnail(yourmodel.image, '430x360', crop=yourmodel.cropping).url


Cropping from a ModelForm
+++++++++++++++++++++++++

If you want to use the cropping widget outside the admin, you'll need to define the ``ImageField`` as
an ``ImageCropField``::

    from django.db import models
    from sorl_cropping import ImageCropField, ImageRatioField

    class MyModel(models.Model):
        image = ImageCropField(blank=True, null=True, upload_to='uploaded_images')
        # size is "width x height"
        cropping = ImageRatioField('image', '430x360')


Alternatively, override the widget in your ModelForm (you just need to do one of these two, not both!)::

    from django import forms
    from sorl_cropping import ImageCropWidget
    
    class MyModelForm(forms.ModelForm):
        class Meta:
            widgets = {
                'image': ImageCropWidget,
            }


Remember to include the form media in the ``<head>`` of your HTML::

    <html>
      <head>
        {{ form.media }}
      </head>
      <body>
        {{ form }}
      </body>
    </html>

The cropping itself happens in the ImageRatioField, the ImageCropField will still be a regular file upload.
If you're selectively including or excluding fields from the ModelForm, remember to include the ImageRatioField.


Extras
------

Multiple formats
++++++++++++++++

If you need the same image in multiple formats, simply specify another ImageRatioField. This will allow the image to be cropped twice::

    from image_cropping import ImageRatioField, ImageCropField

    image = ImageCropField(blank=True, null=True, upload_to='uploaded_images')
    # size is "width x height"
    list_page_cropping = ImageRatioField('image', '200x100')
    detail_page_cropping = ImageRatioField('image', '430x360')


Foreign Keys
++++++++++++

If you need to crop an image contained within another model, referenced by a ForeignKey, the ``ImageRatioField`` is 
composed of the ``ForeignKey`` name, double underscore, and the ``ImageField`` name::

    from django.db import models
    from image_cropping.fields import ImageRatioField

    class Image(models.Model):
        image_field = models.ImageField(upload_to='image/')

    class NewsItem(models.Model):
        title = models.CharField(max_length=255)
        image = models.ForeignKey(Image)
        cropping = ImageRatioField('image__image_field', '120x100')

Cropping foreign keys works only in the admin for now, as it uses the ``raw_id`` widget.


Disabling cropping
++++++++++++++++++

If you want cropping to be optional, use ``allow_fullsize=True`` as an additional keyword argument in your ``ImageRatioField``.
Editors can now switch off cropping by unchecking the checkbox next to the image cropping widget.


Thanks
++++++

This is fork from `django-image-cropping <https://github.com/jonasundderwolf/django-image-cropping>`_
