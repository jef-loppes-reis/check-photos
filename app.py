"""---"""
import tkinter as tk
from os import path, mkdir
from datetime import datetime

from PIL import Image, ImageTk
from pandas import DataFrame, read_excel, read_pickle


class App():

    _path_data = path.join(path.dirname(__file__), 'data')
    _path_temp = path.join(path.dirname(__file__), 'temp')

    if not path.exists(_path_temp):
        mkdir(_path_temp)

    # _df = read_excel('./data/primeira_lista_check.xlsx').head(5)
    _df = read_pickle(f'{_path_data}/primeira_lista_check')
    # _df.iloc[:, 7:] = _df.iloc[:, 7:].astype(bool)
    _df_copy = _df[
            ~((_df.iloc[:, 7]) & \
            (_df.iloc[:, 8]) & \
            (_df.iloc[:, 9]) & \
            (_df.iloc[:, 10]) & \
            (_df.iloc[:, 11]) & \
            (_df.iloc[:, 12]))
        ]

    # Indices
    _current_index: int = list(_df_copy.index)[0]
    _last_index: int = list(_df_copy.index)[0]
    _max_index: int = list(_df_copy.index)[-1:][0]

    # Condições
    _last_data = [False, False, False, False, False, False]

    # Bandeira
    _bandeira = False

    # Criando a janela principal
    _root = tk.Tk()
    _root.title("Tem marca d'agua?")

    # Criando um rótulo para a imagem
    _label_imagem = tk.Label(_root)
    _label_imagem.pack(pady=10)

    # Botões "Sim" e "Não"
    _frame_botoes = tk.Frame(_root)
    _frame_botoes.pack(pady=5)

    _index_label= tk.Label(_root, text="")
    _index_label.pack(side='bottom', anchor='se', padx=10, pady=10)


    def abrir_imagem(self, df_produtos: DataFrame, data: list[bool]):
        print(f"""
              Indice atual: {self._current_index},
              Ultimo indice: {self._last_index},
              Indice maximo: {self._max_index},
              Data atual: {self._last_data}
            """)
        self._index_label.config(text=f"Índice: {self._current_index + 1} de {df_produtos.item_id.count()}")

        df_row = df_produtos.loc[self._current_index].copy()

        imagem = Image.open(df_row['path_img_dowload'])

        image_height = 500
        ratio = image_height / float(imagem.height)
        image_width = int((float(imagem.width) * float(ratio)))
        imagem = imagem.resize((image_width, image_height))

        imagem = ImageTk.PhotoImage(imagem)

        # Exibir a imagem na janela
        self._label_imagem.config(image=imagem)
        self._label_imagem.image = imagem

        if not data is None:
            self.set_values_df(data)
            self.alter_data(data)
        else:
            self.set_values_df([False, False, False, False, False, False])
            self.alter_data([False, False, False, False, False, False])
        


    def sim_marca_agua(self, _df_produtos: DataFrame) -> None:
        # Ação a ser realizada quando o botão "Sim" é clicado
        self.abrir_imagem(df_produtos=_df_produtos, data=[True, False, False, False, False, False])
        if self._bandeira:
            self.aumentar_index()
            self.bandeira(False)
        self.save()


    def nao_marca_agua(self, _df_produtos: DataFrame) -> None:
        # Ação a ser realizada quando o botão "Não" é clicado
        self.abrir_imagem(df_produtos=_df_produtos, data=[False, True, False, False, False, False])
        if self._bandeira:
            self.aumentar_index()
            self.bandeira(False)
        self.save()


    def sim_texto(self, _df_produtos: DataFrame) -> None:
        self.abrir_imagem(df_produtos=_df_produtos, data=[False, False, True, False, False, False])
        if self._bandeira:
            self.aumentar_index()
            self.bandeira(False)
        self.save()


    def nao_texto(self, _df_produtos: DataFrame) -> None:
        self.abrir_imagem(df_produtos=_df_produtos, data=[False, False, False, True, False, False])
        if self._bandeira:
            self.aumentar_index()
            self.bandeira(False)
        self.save()


    def sim_logo(self, _df_produtos: DataFrame) -> None:
        self.abrir_imagem(df_produtos=_df_produtos, data=[False, False, False, False, True, False])
        if self._bandeira:
            self.aumentar_index()
            self.bandeira(False)
        self.save()


    def nao_logo(self, _df_produtos: DataFrame) -> None:
        self.abrir_imagem(df_produtos=_df_produtos, data=[False, False, False, False, False, True])
        if self._bandeira:
            self.aumentar_index()
            self.bandeira(False)
        self.save()


    def reset_data(self, _df_produtos: DataFrame):
        App.alter_data([False, False, False, False, False, False])
        self.abrir_imagem(df_produtos=_df_produtos, data=[False, False, False, False, False, False])
        if self._bandeira:
            self.aumentar_index()
            self.bandeira(False)
        self.save()

##########################################

    def proxima_foto(self, _df_produtos: DataFrame) -> None:
        self.bandeira(True)
        if self._bandeira:
            self.aumentar_index()
            self.bandeira(False)
            self.save()
        self.abrir_imagem(df_produtos=_df_produtos, data=self._last_data)


    def foto_anterior(self, _df_produtos: DataFrame) -> None:
        self.bandeira(True)
        if self._bandeira:
            self.diminuir_index()
            self.bandeira(False)
            self.save()
        self.abrir_imagem(df_produtos=_df_produtos, data=self._last_data)

    def save(self) -> None:
        self._df_copy.to_csv(f'{self._path_temp}/teste.csv', index=False)
        self._df_copy.to_pickle(f'{self._path_temp}/_df_copy_temp')

    @classmethod
    def bandeira(cls, pos: bool):
        cls._bandeira = pos

    @classmethod
    def aumentar_index(cls):
        cls._current_index += 1 if cls._current_index < cls._max_index else cls._max_index

    @classmethod
    def diminuir_index(cls):
        cls._current_index -= 1 if cls._current_index > 0 else 0

    @classmethod
    def alter_data(cls, values: list[bool]):
        cls._last_data = values

    @classmethod
    def last_index(cls):
        cls._last_index = cls._current_index

    @classmethod
    def alter_df(cls) -> None:
        cls._df[cls._df.index.isin(cls._df_copy.index)].iloc[:, 7:] = cls._df_copy.iloc[:, 7:]



    @classmethod
    def set_values_df(cls, valor: list[bool]):
        if valor[0]:
            cls._df_copy.loc[cls._current_index, 'tem_marca_dagua'] = True
            return
        if valor[1]:
            cls._df_copy.loc[cls._current_index, 'nao_tem_marca_dagua'] = True
            return
        if valor[2]:
            cls._df_copy.loc[cls._current_index, 'tem_texto'] = True
            return
        if valor[3]:
            cls._df_copy.loc[cls._current_index, 'nao_tem_texto'] = True
            return
        if valor[4]:
            cls._df_copy.loc[cls._current_index, 'tem_logo'] = True
            return
        if valor[5]:
            cls._df_copy.loc[cls._current_index, 'nao_tem_logo'] = True
            return
        cls._df_copy.loc[cls._current_index, ['tem_marca_dagua', 'nao_tem_marca_dagua',
                                                'tem_texto', 'nao_tem_texto', 'tem_logo',
                                                'nao_tem_logo']] = False


    def main(self):

        # self.alter_data([False, False, False, False, False, False])

        # self.abrir_imagem(self._df_copy,data=self._last_data)

        botao_sim_marca_agua = tk.Button(self._frame_botoes, text="Tem marca d'agua?[Sim]",
            command=lambda : self.sim_marca_agua(self._df_copy))
        botao_sim_marca_agua.pack(side='left', padx=5)

        botao_nao_marca_agua = tk.Button(self._frame_botoes, text="Não tem marca d'agua?[Não]",
            command=lambda : self.nao_marca_agua(self._df_copy))
        botao_nao_marca_agua.pack(side='left', padx=5)

        botao_sim_texto = tk.Button(self._frame_botoes, text='Tem texto?[Sim]',
            command=lambda : self.sim_texto(self._df_copy))
        botao_sim_texto.pack(side='left', padx=5)

        botao_nao_texto = tk.Button(self._frame_botoes, text='Não tem texto?[Não]',
            command=lambda : self.nao_texto(self._df_copy))
        botao_nao_texto.pack(side='left', padx=5)

        botao_sim_logo = tk.Button(self._frame_botoes, text='Tem logo?[Sim]',
            command=lambda : self.sim_logo(self._df_copy))
        botao_sim_logo.pack(side='left', padx=5)

        botao_nao_logo = tk.Button(self._frame_botoes, text='Não tem logo?[Não]',
            command=lambda : self.nao_logo(self._df_copy))
        botao_nao_logo.pack(side='left', padx=5)

        next_button = tk.Button(self._root, text="Próxima foto",
            command=lambda : self.proxima_foto(self._df_copy))
        next_button.pack(side='right', padx=10)

        prev_button = tk.Button(self._root, text="Foto anterior",
            command=lambda : self.foto_anterior(self._df_copy))
        prev_button.pack(side='left', padx=10)

        save_button = tk.Button(self._root, text='Salvar',
            command=self.save)
        save_button.pack(side='left', padx=5)

        reset_button = tk.Button(self._root, text='Resetar',
            command=lambda : self.reset_data(self._df_copy))
        reset_button.pack(side='left', padx=5)

        try:
            self._root.mainloop()
        except Exception:
            self._df.to_excel('results.xlsx')
        finally:
            self._df.to_excel('results.xlsx')



if __name__ == '__main__':

    app = App()
    app.main()
