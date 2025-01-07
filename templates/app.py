import __init__
from views.view import SubscriptionServices
from models.database import engine
from datetime import datetime
from decimal import Decimal
from models.model import Subscription

class UI:
    def __init__(self):
         self.subscription_service = SubscriptionServices(engine)

    def start(self):
        while True:
            print(
                    f"{'-'*60}",
                    "[1] -> Adicionar assinatura",
                    "[2] -> Remover assinatura",
                    "[3] -> Valor total",
                    "[4] -> Gastos últimos 12 meses",
                    "[5] -> Pagar assinatura",
                    "[6] -> Sair", sep='\n'
                    )
            try:
                choice = int(input('Escolha uma opção: '))
            except KeyboardInterrupt:
                print('\n\nEncerrado com sucesso.')
                break
            except ValueError:
                print('\nPor favor, insira numero da opção escolhida\n')
                continue
            if choice == 1:
                self.add_subscription()
            elif choice == 2:
                self.delete_subscription()
            elif choice == 3:
                self.total_value()
            elif choice == 4:
                self.subscription_service.gen_chart()
            elif choice == 5:
                self.pay_subscription()
            else:
                break
    
    def pay_subscription(self):
        empresas = self.subscription_service.list_all()
        subscriptions = self.subscription_service.list_all()
        print('Escolha qual assinatura deseja pagar')
        print(len(subscriptions))
        for enum,i in enumerate(subscriptions):
            print(f'[{enum}] -> {i.empresa}')

        choice = int(input('Escolha a assinatura: '))
        self.subscription_service.pay(subscriptions[choice])
        print('Assinatura paga com sucesso.')

    def add_subscription(self):
        empresa = input('Empresa: ')
        site = input('Site: ')
        data_assinatura = datetime.strptime(input('Data de assinatura (dd/mm/yyyy): '), '%d/%m/%Y')
        valor = Decimal(input('Valor: '))

        subscription = Subscription(empresa=empresa, site=site, data_assinatura=data_assinatura, valor=valor)
        self.subscription_service.create(subscription)
        print('Assinatura adicionada com sucesso.')

    def delete_subscription(self):
        subscriptions = self.subscription_service.list_all()
        print('Escolha qual assinatura deseja excluir')

        for i in subscriptions:
            print(f'[{i.id}] -> {i.empresa}')

        choice = int(input('Escolha a assinatura: '))
        self.subscription_service.delete(choice)
        print('Assinatura excluída com sucesso.')

    def total_value(self):
        print(f'Seu valor total mensal em assinaturas: {self.subscription_service.total_value()}')
        input('\n\nEnter para continuar...')


if __name__ == "__main__":
    UI().start()
