from django.shortcuts import render, reverse, get_object_or_404, HttpResponseRedirect, redirect
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from .models import Vendor, Invoice, Payment, Employer, PaymentMethod, VendorBankingAccount, Note
from .forms import InvoiceVendorDetailForm, EmployerForm, PaymentForm, InvoiceForm, VendorBankingAccountForm, NoteForm


@staff_member_required
def validate_invoice_form_view(request, pk):
    vendor = get_object_or_404(Vendor, id=pk)
    form = InvoiceVendorDetailForm(request.POST or None, initial={'vendor': vendor})
    if form.is_valid():
        new_instance = form.save()
        messages.success(request, f'Το παραστατικό {new_instance.title} δημιουργηθηκε.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def validate_payment_form_view(request, pk):
    vendor = get_object_or_404(Vendor, id=pk)
    form = PaymentForm(request.POST or None, initial={'vendor': vendor})
    if form.is_valid():
        new_instance = form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def validate_employer_view(request, pk):
    vendor = get_object_or_404(Vendor, id=pk)
    form = EmployerForm(request.POST or None, initial={'vendor': vendor})
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def validate_invoice_edit_form_view(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    form = InvoiceForm(request.POST or None, instance=invoice)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def delete_invoice_view(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    invoice.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def validate_payment_edit_form_view(request, pk):
    invoice = get_object_or_404(Payment, id=pk)
    form = PaymentForm(request.POST or None, instance=invoice)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def delete_payment_view(request, pk):
    invoice = get_object_or_404(Payment, id=pk)
    invoice.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def validate_employer_edit_view(request, pk):
    employer = get_object_or_404(Employer, id=pk)
    form = EmployerForm(request.POST or None, instance=employer)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def delete_employer_view(request, pk):
    employer = get_object_or_404(Employer, id=pk)
    employer.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def validate_create_banking_account_view(request, pk):
    vendor = get_object_or_404(Vendor, id=pk)
    form = VendorBankingAccountForm(request.POST, initial={'vendor': vendor})
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def validate_edit_banking_account_view(request, pk):
    banking_account = get_object_or_404(VendorBankingAccount, id=pk)
    form = VendorBankingAccountForm(request.POST or None, instance=banking_account)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def delete_banking_account_view(request, pk):
    banking_account = get_object_or_404(VendorBankingAccount, id=pk)
    banking_account.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def validate_note_creation_view(request, pk):
    instance = get_object_or_404(Vendor, id=pk)
    form = NoteForm(request.POST or None, initial={'vendor_related': instance})
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))






