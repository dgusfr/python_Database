from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import create_engine, String, Text, select, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column, relationship

engine = create_engine(
    "sqlite:///:memory:", echo=True
)  # echo=True é usado para mostrar as consultas SQL geradas pelo SQLAlchemy no console, isso é útil para depuração e aprendizado


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    # Mapped define os tipos de dados que estão sendo usados
    # mapped_column é usado para definir as colunas do banco de dados,nesta versão do sqlalchemy não é mais usado nullable, mas sim o tipo de dado do campo, se for Optional é porque pode ser nulo
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))  # essa string suporta 50 caracteres
    last_login: Mapped[Optional[datetime]]

    posts: Mapped[list["Post"]] = relationship(
        back_populates="author"
    )  # backpopulates é usado para criar um relacionamento bidirecional entre as tabelas, ou seja, quando você acessar o atributo posts de um usuário, ele vai retornar uma lista de posts relacionados a esse usuário, e quando você acessar o atributo author de um post, ele vai retornar o usuário relacionado a esse post

    # __repr__ imprime o objeto criado
    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, last_login={self.last_login})"


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(
        String(50), default="Untitled"
    )  # default, se não preenchido o valor será "Untitled"
    content: Mapped[str] = mapped_column(
        Text
    )  # Text é usado para campos de texto longo
    author_id: Mapped[int] = mapped_column(
        ForeignKey("user.id")
    )  # ForeignKey é usado para criar uma chave estrangeira, ou seja, um campo que referencia a chave primária de outra tabela

    user: Mapped["User"] = relationship(back_populates="posts")

    def __repr__(self):
        return f"Post(id={self.id}, title={self.title}"


# ------- Criando as tabelas no banco de dados -------
Base.metadata.create_all(engine)

with Session(engine) as session:
    anthony = User(name="Anthony", last_login=datetime.now(timezone.utc))
    mary = User(name="Mary")

    session.add_all([anthony, mary])
    session.commit()
    session.refresh(anthony)
    session.refresh(mary)

    # Consultando os usuários
    stmt = select(User)
    # scalars é usado para retornar os objetos do tipo User, e all() é usado para retornar todos os resultados da consulta, ou seja, todos os usuarios
    users = session.scalars(stmt).all()
    for user in users:
        print(user)
        for post in user.posts:
            print(post)

    # 2ª consulta, por id
    anthony = session.get(
        User, 1
    )  # get é usado para buscar um objeto pelo seu id, nesse caso, o id do anthony é 1
    if anthony:
        print(anthony)

    # 3ª consulta, com Where
    stmt = select(User).where(User.name == "Mary")
    mary = session.scalars(
        stmt
    ).first()  # first() é usado para retornar o primeiro resultado da consulta, nesse caso, o usuário Mary
    if mary:
        print(f"User found: {mary}")

    # 4ª consulta, com Where e Order By, nesse caso, estamos buscando os posts do anthony, ordenando por id de forma decrescente
    stmt = select(Post).where(Post.user == anthony).order_by(Post.id.desc())
    posts = session.scalars(stmt).all()
    for post in posts:
        print(post)
        print(f"Author: {post.user.name}")


# Diferença entre versão antiga do SQLAlchemy e a nova versão:
# Na versão antiga, as colunas eram definidas usando o tipo de dado diretamente, como Integer, String, etc. Já na nova versão, as colunas são definidas usando o tipo de dado do campo, como Mapped[int], Mapped[str], etc.
# A nova versão as consultas são definidas independentemente da sessão e depois executadas usando a sessão, enquanto na versão antiga as consultas eram definidas diretamente na sessão.
