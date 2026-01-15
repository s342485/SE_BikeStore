from database.dao import DAO
from model.model import Model

dao = DAO()

model = Model()
categoria = "Children Bicycles"

risultato = dao.get_all_nomi_prodotti()
for risultato in risultato:
    print(risultato)

