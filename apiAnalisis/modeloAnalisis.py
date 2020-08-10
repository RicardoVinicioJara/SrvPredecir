import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.compose import make_column_transformer
from sklearn import preprocessing
import matplotlib.pyplot as plt



class Cliente():
    def __init__(self, DNI, PLAZOMESESCREDITO, HISTORIALCREDITO, PROPOSITOCREDITO, MONTOCREDITO, SALDOCUENTAAHORROS,
                 TIEMPOEMPLEO, TASAPAGO, ESTADOCIVILYSEXO, GARANTE, AVALUOVIVIENDA, ACTIVOS, EDAD, VIVIENDA,
                 CANTIDADCREDITOSEXISTENTES, EMPLEO, TRABAJADOREXTRANJERO, TIPOCLIENTE):
        self.DNI = DNI
        self.PLAZOMESESCREDITO = PLAZOMESESCREDITO
        self.HISTORIALCREDITO = HISTORIALCREDITO
        self.PROPOSITOCREDITO = PROPOSITOCREDITO
        self.MONTOCREDITO = MONTOCREDITO
        self.SALDOCUENTAAHORROS = SALDOCUENTAAHORROS
        self.TIEMPOEMPLEO = TIEMPOEMPLEO
        self.TASAPAGO = TASAPAGO
        self.ESTADOCIVILYSEXO = ESTADOCIVILYSEXO
        self.GARANTE = GARANTE
        self.AVALUOVIVIENDA = AVALUOVIVIENDA
        self.ACTIVOS = ACTIVOS
        self.EDAD = EDAD
        self.VIVIENDA = VIVIENDA
        self.CANTIDADCREDITOSEXISTENTES = CANTIDADCREDITOSEXISTENTES
        self.EMPLEO = EMPLEO
        self.TRABAJADOREXTRANJERO = TRABAJADOREXTRANJERO
        self.TIPOCLIENTE = TIPOCLIENTE

    def __str__(self):
        return self.DNI + " <> " + self.TIEMPOEMPLEO


class modeloAnalisis():
    def __init__(self):
        pass

    """Clase modelo Analisis"""
    dfOriginal = pd.DataFrame([])
    DataframeTransformado1 = pd.DataFrame([])

    def getPastel(self, buenos, malos, definir):
        manzanas = [buenos, malos, definir]
        nombres = ["CLientes Buenos", "Clientes Malos", "Clientes por definir"]
        desfase = (0, 0, 0.1)
        plt.pie(manzanas, labels=nombres, autopct="%0.1f %%", explode=desfase)
        plt.savefig("apiAnalisis/pastel2.png")
        print('Guardando.... Pastel')

    def getImg(self):
        self.dfOriginal = pd.read_csv('apiAnalisis/DatasetBanco.csv', sep=";")
        self.DataframeTransformado1 = pd.read_csv('apiAnalisis/5.DatasetBancoTransformadoMinMax.csv', sep=";")
        buenos = 0;
        malos = 0;
        for row in self.dfOriginal.DNI:
            print(row)
            res = self.predecir(self, row)
            if res == '1':
                buenos += 1
            else:
                malos += 1
        manzanas = [buenos, malos]
        nombres = ["CLientes Buenos", "Clientes Malos"]
        desfase = (0, 0.1)
        plt.pie(manzanas, labels=nombres, autopct="%0.1f %%", explode=desfase)
        plt.savefig("apiAnalisis/pastel.png")
        print('Guardando....')

    def addRow(self, c=Cliente):
        self.dfOriginal = pd.read_csv('apiAnalisis/DatasetBanco.csv', sep=";")
        dataframe = self.dfOriginal
        add_row = pd.Series(
            [int(c.DNI), c.PLAZOMESESCREDITO, c.HISTORIALCREDITO, c.PROPOSITOCREDITO, c.MONTOCREDITO, c.SALDOCUENTAAHORROS,
             c.TIEMPOEMPLEO, c.TASAPAGO, c.ESTADOCIVILYSEXO, c.GARANTE, c.AVALUOVIVIENDA, c.ACTIVOS, c.EDAD, c.VIVIENDA,
             c.CANTIDADCREDITOSEXISTENTES, c.EMPLEO, c.TRABAJADOREXTRANJERO, c.TIPOCLIENTE],
            index=['DNI', 'PLAZOMESESCREDITO', 'HISTORIALCREDITO', 'PROPOSITOCREDITO', 'MONTOCREDITO', 'SALDOCUENTAAHORROS',
                 'TIEMPOEMPLEO', 'TASAPAGO', 'ESTADOCIVILYSEXO', 'GARANTE', 'AVALUOVIVIENDA', 'ACTIVOS', 'EDAD', 'VIVIENDA',
                 'CANTIDADCREDITOSEXISTENTES', 'EMPLEO', 'TRABAJADOREXTRANJERO', 'TIPOCLIENTE'])

        cliente = self.dfOriginal.loc[self.dfOriginal['DNI'] == int(c.DNI)]
        if not cliente.empty:
            self.dfOriginal.drop(cliente, axis=1)
            print("Eliminado.....")
        rest = dataframe.append(add_row, ignore_index=True)
        rest.to_csv("apiAnalisis/DatasetBanco.csv", sep=";", index=False)


    def predecirTipoCliente(self, Dni=0):
        print('Dni:', Dni)
        self.preprocesamiento(self)
        tipoCliente = self.predecir(self, Dni)
        # tipoCliente = '1'
        if tipoCliente == '1':
            # mensaje='Dni:',Dni,', es un buen cliente.'
            mensaje = "1"
            # dbReg = models.Cliente(cedula=Dni, edad=edad, tipoCliente=tipoCliente)
            # dbReg.save()
        elif tipoCliente == '2':
            # mensaje='Dni:',Dni,', es un mal cliente'
            mensaje = "2"
            # dbReg =models.Cliente(cedula=Dni, edad=edad, tipoCliente=tipoCliente)
            # dbReg.save()
        else:
            mensaje = 'No existe el cliente con Dni:' + str(Dni)
        return mensaje

    def predecir(self, Dni=0):
        print(Dni)
        cliente = self.dfOriginal.loc[self.dfOriginal['DNI'] == Dni]
        if not (cliente.empty):
            print('Existe el cliente')
            indiceCliente = cliente.index.values[0]
            edad = cliente['EDAD'].values
            edad = edad[0]
            print('Indice: ', indiceCliente)
            cliente = self.DataframeTransformado1.loc[indiceCliente, :]
            historialCredito = round(cliente[0], 2)
            saldoAhorros = round(cliente[1], 2)
            tiempoEmpleo = round(cliente[2], 2)
            activos = round(cliente[4], 2)
            if activos < 0.5 and edad > 25 and (historialCredito < 0.5 or saldoAhorros > 0.5 or tiempoEmpleo > 0.5):
                tipoCliente = '1'
            else:
                tipoCliente = '2'
        else:
            tipoCliente = '3'
        return tipoCliente

    def preprocesamiento(self):
        # os.path.join(THIS_FOLDER, 'myfile.txt')
        self.dfOriginal = pd.read_csv('apiAnalisis/DatasetBanco.csv', sep=";")
        dataframe = self.dfOriginal
        # print(self.dfOriginal)
        salida = self.dfOriginal.TIPOCLIENTE.values
        dataframe = dataframe.drop(['DNI'], axis=1)
        dataframe = dataframe.drop(["TIPOCLIENTE"], axis=1)
        # print(dataframe.shape)
        categorical_ordinal = ['HISTORIALCREDITO', 'SALDOCUENTAAHORROS', 'TIEMPOEMPLEO', 'ESTADOCIVILYSEXO', 'ACTIVOS'
            , 'VIVIENDA', 'EMPLEO']
        categorical_nominal = ['PROPOSITOCREDITO', 'GARANTE', 'TRABAJADOREXTRANJERO']
        numerical = ['PLAZOMESESCREDITO', 'MONTOCREDITO', 'TASAPAGO', 'AVALUOVIVIENDA', 'EDAD'
            , 'CANTIDADCREDITOSEXISTENTES']
        preprocesador1 = make_column_transformer(
            (OrdinalEncoder(), categorical_ordinal),
            (OneHotEncoder(sparse=False), categorical_nominal),
            remainder='passthrough'
        )

        X = preprocesador1.fit_transform(dataframe)
        np.set_printoptions(formatter={'float': lambda X: "{0:0.0f}".format(X)})
        cnamesDataset1 = categorical_ordinal
        cnamesDataset2 = preprocesador1.transformers_[1][1].get_feature_names(categorical_nominal)
        cnamesDataset3 = numerical
        cnamesDataset1.extend(cnamesDataset2)
        cnamesDataset1.extend(cnamesDataset3)

        DataframePreprocesado = pd.DataFrame(data=X, columns=cnamesDataset1)
        DataframePreprocesado = pd.concat([DataframePreprocesado, self.dfOriginal[['TIPOCLIENTE']]], axis=1)
        DataframePreprocesado.to_csv("apiAnalisis/4.DatasetBancoPreprocesado.csv", sep=";", index=False)

        cr = DataframePreprocesado.corr()
        cr = round(cr, 3)
        DataframePreprocesado = DataframePreprocesado.drop(['TIPOCLIENTE'], axis=1)
        data_scaler_minmax = preprocessing.MinMaxScaler(feature_range=(0, 1))
        data_scaled_minmax = data_scaler_minmax.fit_transform(DataframePreprocesado)

        self.DataframeTransformado1 = pd.DataFrame(data=data_scaled_minmax, columns=cnamesDataset1)
        self.DataframeTransformado1 = pd.concat([self.DataframeTransformado1, self.dfOriginal[['TIPOCLIENTE']]], axis=1)
        self.DataframeTransformado1.to_csv("apiAnalisis/5.DatasetBancoTransformadoMinMax.csv", sep=";",
                                           index=False)  # sep es el separado, por defector es ","
        return "listo"
