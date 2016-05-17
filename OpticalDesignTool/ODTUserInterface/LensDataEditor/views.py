from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Surface, RaySet
from .forms import SurfaceEditorForm, OpSurfaceForm, RaysetEditorForm
from django.forms import formset_factory, BaseModelFormSet
import json


def editSurfaceSet(request):

    return render(request, 'LensDataEditor/editSurfaceSet.html')

def rayData(request):
    ordered_raysets = RaySet.objects.order_by('raySetIndex')
    RaySetType = formset_factory(RaysetEditorForm, extra=0)
    pk_list = [rayset.pk for rayset in ordered_raysets]

    if len(ordered_raysets) == 0:
        rayset = RaySet()
        rayset.raySetIndex = 1
        rayset.raySetGridType = 'Radial'

        rayset.save()
        ordered_raysets = RaySet.objects.order_by('raySetIndex')

    if request.method == 'POST':
        if 'Update' in request.POST:
            formSet = RaySetType(request.POST)

            if formSet.is_valid():
                pk_index = 0
                for form in formSet:
                    if pk_index < len(pk_list):
                        rayset = RaySet.objects.get(pk=pk_list[pk_index])
                    else:
                        rayset = RaySet()

                    for key in form.cleaned_data:
                        setattr(rayset, key, form.cleaned_data[key])
                    rayset.save()
                    pk_index += 1

        elif 'Add' in request.POST:
            rayset = RaySet()
            rayset.raySetIndex = max([x.raySetIndex for x in ordered_raysets]) + 1
            rayset.save()

        elif 'Delete' in request.POST:
            deleteIndex = int(request.POST['opSurfaceIndex'])
            deleteList = []

            for rayset in ordered_raysets:
                if rayset.raySetIndex == deleteIndex:
                    deleteList.append(rayset.pk)
            indexChange = len(deleteList)
            for rayset in ordered_raysets:
                if rayset.raySetIndex > deleteIndex:
                    rayset.raySetIndex -= indexChange
                    rayset.save()

            for deletepk in deleteList:
                rayset = RaySet.objects.get(pk=deletepk)
                rayset.delete()

        return HttpResponseRedirect('/LensDataEditor/EditSurfaceSet/RayData/')
    else:
        data = [rayset.__dict__ for rayset in ordered_raysets]
        RaysetForm = RaySetType(initial=data)
        form2 = OpSurfaceForm()

    return render(request, 'LensDataEditor/editRaySet.html', {'formSet': RaysetForm, 'form2': form2})

def meritFunction(request):
    if request.method == 'POST':
        pass
    else:
        pass

    return render(request, 'LensDataEditor/editMerit.html')

def configData(request):
    if request.method == 'POST':
        pass
    else:
        pass

    return render(request, 'LensDataEditor/editConfig.html')


def lensData(request):

    ordered_query = Surface.objects.order_by('surfaceIndex')

    pk_list = [surface.pk for surface in ordered_query]

    FormSetType = formset_factory(SurfaceEditorForm, extra=0)

    if request.method == 'POST':

        if 'Update' in request.POST:
            formSet = FormSetType(request.POST)
            if formSet.is_valid():
                print(formSet.cleaned_data)
                pk_index = 0
                for form in formSet:
                    if pk_index < len(pk_list):
                        surface = Surface.objects.get(pk=pk_list[pk_index])
                    else:
                        surface = Surface()

                    for key in form.cleaned_data:
                        setattr(surface, key, form.cleaned_data[key])
                    surface.save()
                    pk_index += 1
            else:
                print('Not Clean')
        elif 'Add' in request.POST:
            insertIndex = int(request.POST['opSurfaceIndex'])

            newSurface = Surface()
            if (~insertIndex) and (insertIndex <= ordered_query[-1].surfaceIndex):
                for surface in ordered_query:
                    if surface.surfaceIndex > insertIndex:
                        surface.surfaceIndex += 1
                        surface.save()
                newSurface.surfaceIndex = insertIndex + 1
            else:
                newSurface.surfaceIndex = ordered_query[-1].surfaceIndex + 1

            newSurface.save()

        elif 'Delete' in request.POST:
            deleteIndex = int(request.POST['opSurfaceIndex'])
            deleteList = []

            for surface in ordered_query:
                if surface.surfaceIndex == deleteIndex:
                    deleteList.append(surface.pk)

            for surface in ordered_query:
                if surface.surfaceIndex > deleteIndex:
                    surface.surfaceIndex -= len(deleteList)
                    surface.save()

            for deletepk in deleteList:
                surface = Surface.objects.get(pk=deletepk)
                surface.delete()

        return HttpResponseRedirect('/LensDataEditor/EditSurfaceSet/LensData/')

    else:
        data = [surface.__dict__ for surface in ordered_query]
        formSet = FormSetType(initial=data)
        form2 = OpSurfaceForm()

        lensData = [datum for datum in data]
        for datum in lensData:
            datum.pop('_state')

    return render(request, 'LensDataEditor/lensData.html', {'formSet': formSet, 'form2': form2 , 'lensData': json.dumps(lensData)})