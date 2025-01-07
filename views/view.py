import __init__
from models.database import engine
from models.model import Subscription, Payments
from datetime import date, timedelta
from sqlmodel import Session, select

class SubscriptionServices:
    def __init__(self, engine):
        self.engine = engine
    
    def create(self, subsciption: Subscription):
        with Session(self.engine) as session:
            session.add(subsciption)
            session.commit()
            return subsciption

    def list_all(self):
        with Session(self.engine) as session:
            statement = select(Subscription)
            results = session.exec(statement).all()
        return results
    
    def _has_pay(self, results) -> bool:
        for result in results:
            if result.date.month == date.today().month:
                return True
        return False

    def pay(self, subscription: Subscription):
        with Session(self.engine) as session:
            statement = select(Payments).join(Subscription).where(Subscription.id==subscription.id)
            results = session.exec(statement).all()
            
            
            if self._has_pay(results):
                question = input(
                    'esta conta já foi paga neste mês, gostaria de pagar novamente? [Y/N]: '
                )
                if not question.upper() == "Y":
                    return
            pay = Payments(subscription_id=subscription.id, date=date.today())
            session.add(pay)
            session.commit()

    def total_value(self):
        with Session(self.engine) as session:
            statement = select(Subscription)
            results = session.exec(statement).all()

            total=0
            for result in results:
                total+=result.valor
                print(f'{float(result.valor)}', f' --- {result.empresa}')
            print("-"*20, total, sep='\n')
            return float(total)
    
    def delete(self, id):
        self._delete_all_payments(id)
        with Session(self.engine) as session:
            statement = select(Subscription).where(Subscription.id == id)
            result = session.exec(statement).one()
            session.delete(result)
            session.commit()

    def _delete_all_payments(self, id):
        with Session(self.engine) as session:
            statement = select(Payments).join(Subscription).where(Subscription.id == id)
            results = session.exec(statement).all()
            if results:
                for pay in results:
                    session.delete(pay)
            session.commit()
            print('payments de conta id %s deletado com sucesso' % id)
    
    def _get_last_12_months_native(self):
        today = date.today()
        year = today.year
        month = today.month
        last_12_months = []
        for _ in range(12):
            last_12_months.append((month, year))
            month -= 1
            if month == 0:
                month = 12
                year -= 1
        return last_12_months[::-1]
    
    def _get_values_for_months(self, last_12_months):
        with Session(self.engine) as session:
            statement = select(Payments)
            results = session.exec(statement).all()

            value_for_months = []
            for i in last_12_months:
                value = 0
                for result in results:
                    if result.date.month == i[0] and result.date.year == i[1]:
                        value += float(result.subscription.valor)

                value_for_months.append(value)
        return value_for_months
    
    def gen_chart(self):
        last_12_months = self._get_last_12_months_native()
        values_for_months = self._get_values_for_months(last_12_months)

        name_months: list[str] = []
        # pega o nome dos meses
        for i in last_12_months:
            name_months.append(f'{date(year=i[1], month=i[0], day=1).strftime('%b/%y')}')

        import matplotlib.pyplot as plt
        last_12_months = list(range(1,13))
        plt.plot(last_12_months, values_for_months, marker='o')
        
        # formatar campos
        plt.xticks(last_12_months[::-2], name_months[::-2])
        plt.xlabel('Mês')
        plt.ylabel('Valor')
        plt.title('Gastos Mensais')
        plt.grid(True)
        plt.show()
