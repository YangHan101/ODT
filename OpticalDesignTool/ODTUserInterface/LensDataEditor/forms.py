__author__ = 'yanghan1'

from django import forms

class SurfaceEditorForm(forms.Form):

        options = (('Window', 'Window'),
                   ('Mirror', 'Mirror'),
                   ('Beamsplitter', 'Beamsplitter'),
                   ('Source', 'Source'),
                   ('Image', 'Image'))
        surfaceIndex = forms.IntegerField(
            label='#',
            widget=forms.NumberInput(attrs={'style': 'width:30px'})
        )

        surfaceType = forms.ChoiceField(choices=options)
        # surfaceType.widget = forms.Select(attrs={'style': 'width:200px'})

        surfaceMaterial = forms.CharField(
            max_length=20,
            widget=forms.TextInput(attrs={'style': 'width:80px'})
        )

        surfaceMaterialOptable = forms.BooleanField(required=False)

        surfaceRadius = forms.FloatField(
            label='R',
            widget=forms.TextInput(attrs={'style': 'width:80px'})
        )
        surfaceRadiusOptable = forms.BooleanField(required=False)

        surfaceVertexCurvature = forms.FloatField(
            label='Curvature',
            widget=forms.TextInput(attrs={'style': 'width:80px'})
        )

        surfaceVertexCurvatureOptable = forms.BooleanField(required=False)

        surfaceConicConstant = forms.FloatField(
            label='Conic',
            widget=forms.TextInput(attrs={'style': 'width:80px'})
        )
        surfaceConicConstantOptable = forms.BooleanField(required=False)

        surfaceDecenterX = forms.FloatField(
            label='dX',
            widget=forms.TextInput(attrs={'style': 'width:80px'}))
        surfaceDecenterXOptable = forms.BooleanField(required=False)

        surfaceDecenterY = forms.FloatField(
            label='dY',
            widget=forms.TextInput(attrs={'style': 'width:80px'})
        )
        surfaceDecenterYOptable = forms.BooleanField(required=False)

        surfaceThickness = forms.FloatField(
            label='Thickness',
            widget=forms.TextInput(attrs={'style': 'width:80px'})
        )
        surfaceThicknessOptable = forms.BooleanField(required=False)


class OpSurfaceForm(forms.Form):
    opSurfaceIndex = forms.IntegerField(label='')

class RaysetEditorForm(forms.Form):

        options = (('Radial', 'Radial'),
                   ('Triangular', 'Triangular'),
                   ('RandomMesh', 'RandomMesh'))

        raySetIndex = forms.IntegerField(
            label='#',
            widget=forms.NumberInput(attrs={'style': 'width:30px'})
        )

        raySetGridType = forms.ChoiceField(choices=options)
        raySetGridDensity = forms.IntegerField(
            label='Grid Density',
            widget=forms.NumberInput(attrs={'style': 'width:100px'})
        )

        raySetAngleX = forms.FloatField(
            label='Tilt X',
            widget=forms.TextInput(attrs={'style': 'width:100px'}))

        raySetAngleY = forms.FloatField(
            label='Tilt Y',
            widget=forms.TextInput(attrs={'style': 'width:100px'})
        )

        raySetWavelength = forms.FloatField(
            label='Wavelength(um)',
            widget=forms.TextInput(attrs={'style': 'width:100px'}))