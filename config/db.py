from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://USUARIO:CONTRASEÑA@IP:3306", echo=True)

meta_data = MetaData()
meta_data.create_all(engine)
