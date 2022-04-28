from django.urls import path

from .views import AnalysisHomepage, AnalysisIncomeView, AnalysisOutcomeView, CashRowView, BalanceSheetView, AnalysisReservationView

app_name='analysis'

urlpatterns = [
    path('homepage/', AnalysisHomepage.as_view(), name='homepage'),
    path('incomes/', AnalysisIncomeView.as_view(), name='income_analysis'),
    path('outcomes/', AnalysisOutcomeView.as_view(), name='outcome_analysis'),
    path('cash-row/', CashRowView.as_view(), name='cash_row'),
    path('balance-sheet/', BalanceSheetView.as_view(), name='balance_sheet'),
    path('reservations/analysis/', AnalysisReservationView.as_view(), name='reservation_analysis'),

    
]