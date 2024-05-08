import tkinter as tk
from tkinter import ttk
from utils import get_historical_data, plot_historical_data, convert_currencies, predict_currency_rate

class CurrencyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Валютный конвертер")
        self.geometry("400x300")

        # Создаем вкладки
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", padx=10, pady=10)

        # Вкладка "Получить данные"
        self.tab_get_data = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_get_data, text="Получить данные")
        self.create_get_data_tab()

        # Вкладка "График"
        self.tab_plot = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_plot, text="График")
        self.create_plot_tab()

        # Вкладка "Конвертер"
        self.tab_convert = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_convert, text="Конвертер")
        self.create_convert_tab()

        # Вкладка "Прогноз курса"
        self.tab_predict = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_predict, text="Прогноз курса")
        self.create_predict_tab()

    def create_predict_tab(self):
        currency_label = ttk.Label(self.tab_predict, text="Валюта:")
        currency_label.grid(row=0, column=0, padx=5, pady=5)
        self.currency_entry = ttk.Entry(self.tab_predict)
        self.currency_entry.grid(row=0, column=1, padx=5, pady=5)

        predict_button = ttk.Button(self.tab_predict, text="Прогноз курса", command=self.predict_rate)
        predict_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.prediction_label = ttk.Label(self.tab_predict, text="")
        self.prediction_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def predict_rate(self):
        currency = self.currency_entry.get().upper()
        try:
            prediction = predict_currency_rate(currency)
            self.prediction_label.config(text=prediction)
        except Exception as e:
            self.prediction_label.config(text=str(e))


    def create_get_data_tab(self):
        start_date_label = ttk.Label(self.tab_get_data, text="Начальная дата (ГГГГ-ММ-ДД):")
        start_date_label.grid(row=0, column=0, padx=5, pady=5)
        self.start_date_entry = ttk.Entry(self.tab_get_data)
        self.start_date_entry.grid(row=0, column=1, padx=5, pady=5)

        end_date_label = ttk.Label(self.tab_get_data, text="Конечная дата (ГГГГ-ММ-ДД):")
        end_date_label.grid(row=1, column=0, padx=5, pady=5)
        self.end_date_entry = ttk.Entry(self.tab_get_data)
        self.end_date_entry.grid(row=1, column=1, padx=5, pady=5)

        currency_label = ttk.Label(self.tab_get_data, text="Валюта:")
        currency_label.grid(row=2, column=0, padx=5, pady=5)
        self.currency_entry = ttk.Entry(self.tab_get_data)
        self.currency_entry.grid(row=2, column=1, padx=5, pady=5)

        get_data_button = ttk.Button(self.tab_get_data, text="Получить данные", command=self.get_data)
        get_data_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.data_text = tk.Text(self.tab_get_data, height=10, width=60)
        self.data_text.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def create_plot_tab(self):
        start_date_label = ttk.Label(self.tab_plot, text="Начальная дата (ГГГГ-ММ-ДД):")
        start_date_label.grid(row=0, column=0, padx=5, pady=5)
        self.plot_start_date_entry = ttk.Entry(self.tab_plot)
        self.plot_start_date_entry.grid(row=0, column=1, padx=5, pady=5)

        end_date_label = ttk.Label(self.tab_plot, text="Конечная дата (ГГГГ-ММ-ДД):")
        end_date_label.grid(row=1, column=0, padx=5, pady=5)
        self.plot_end_date_entry = ttk.Entry(self.tab_plot)
        self.plot_end_date_entry.grid(row=1, column=1, padx=5, pady=5)

        currency_label = ttk.Label(self.tab_plot, text="Валюта:")
        currency_label.grid(row=2, column=0, padx=5, pady=5)
        self.plot_currency_entry = ttk.Entry(self.tab_plot)
        self.plot_currency_entry.grid(row=2, column=1, padx=5, pady=5)

        plot_button = ttk.Button(self.tab_plot, text="Построить график", command=self.plot_data)
        plot_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def create_convert_tab(self):
        from_currency_label = ttk.Label(self.tab_convert, text="Из валюты:")
        from_currency_label.grid(row=0, column=0, padx=5, pady=5)
        self.from_currency_entry = ttk.Entry(self.tab_convert)
        self.from_currency_entry.grid(row=0, column=1, padx=5, pady=5)

        to_currency_label = ttk.Label(self.tab_convert, text="В валюту:")
        to_currency_label.grid(row=1, column=0, padx=5, pady=5)
        self.to_currency_entry = ttk.Entry(self.tab_convert)
        self.to_currency_entry.grid(row=1, column=1, padx=5, pady=5)

        convert_button = ttk.Button(self.tab_convert, text="Конвертировать", command=self.convert_currencies)
        convert_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.result_text = tk.Text(self.tab_convert, height=10, width=60)
        self.result_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)


    def get_data(self):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        currency = self.currency_entry.get()
        historical_data = get_historical_data(start_date, end_date, currency)
        self.data_text.delete("1.0", "end")
        for date, price in historical_data.items():
            self.data_text.insert("end", f"{date} стоимость валюты к рублю составила {price}\n")

    def plot_data(self):
        start_date = self.plot_start_date_entry.get()
        end_date = self.plot_end_date_entry.get()
        currency = self.plot_currency_entry.get()
        plot_historical_data(start_date, end_date, currency)

    def convert_currencies(self):
        from_currency = self.from_currency_entry.get()
        to_currency = self.to_currency_entry.get()
        result = convert_currencies(from_currency, to_currency)

        self.result_text.delete("1.0", "end")  # Очистить текстовое поле перед вставкой

        # Разделить result на отдельные строки и вставить их по одной
        for line in result.split("\n"):
            self.result_text.insert("end", line + "\n")


app = CurrencyApp()
app.mainloop()