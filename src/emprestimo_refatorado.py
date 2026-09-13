from abc import ABC, abstractmethod
import sqlite3
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from reportlab.pdfgen import canvas


class IRepositorio(ABC):
    @abstractmethod
    def buscar(self, id):
        pass

    @abstractmethod
    def salvar(self, entidade):
        pass


class RepositorioLivro(IRepositorio):
    def __init__(self, db_path):
        self.db_path = db_path

    def conectar(self):
        return sqlite3.connect(self.db_path)

    def buscar(self, isbn):
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute(
            """SELECT isbn, titulo, autor, categoria, exemplares_disponiveis
               FROM livros
               WHERE isbn = ?""",
            (isbn,)
        )

        resultado = cursor.fetchone()
        conn.close()

        if resultado is None:
            return None

        return {
            "isbn": resultado[0],
            "titulo": resultado[1],
            "autor": resultado[2],
            "categoria": resultado[3],
            "exemplares_disponiveis": resultado[4]
        }

    def salvar(self, livro):
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute(
            """UPDATE livros
               SET exemplares_disponiveis = ?
               WHERE isbn = ?""",
            (
                livro["exemplares_disponiveis"],
                livro["isbn"]
            )
        )

        conn.commit()
        conn.close()


class RepositorioLeitor(IRepositorio):
    def __init__(self, db_path):
        self.db_path = db_path

    def conectar(self):
        return sqlite3.connect(self.db_path)

    def buscar(self, cpf):
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute(
            """SELECT cpf, nome, email, telefone
               FROM leitores
               WHERE cpf = ?""",
            (cpf,)
        )

        resultado = cursor.fetchone()
        conn.close()

        if resultado is None:
            return None

        return {
            "cpf": resultado[0],
            "nome": resultado[1],
            "email": resultado[2],
            "telefone": resultado[3]
        }

    def salvar(self, leitor):
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute(
            """INSERT INTO leitores (cpf, nome, email, telefone)
               VALUES (?, ?, ?, ?)""",
            (
                leitor["cpf"],
                leitor["nome"],
                leitor["email"],
                leitor["telefone"]
            )
        )

        conn.commit()
        conn.close()


class RepositorioEmprestimo(IRepositorio):
    def __init__(self, db_path):
        self.db_path = db_path

    def conectar(self):
        return sqlite3.connect(self.db_path)

    def buscar(self, id):
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute(
            """SELECT id, livro_isbn, leitor_cpf,
                      data_emprestimo, data_devolucao_prevista,
                      data_devolucao
               FROM emprestimos
               WHERE id = ?""",
            (id,)
        )

        resultado = cursor.fetchone()
        conn.close()

        if resultado is None:
            return None

        return {
            "id": resultado[0],
            "livro_isbn": resultado[1],
            "leitor_cpf": resultado[2],
            "data_emprestimo": resultado[3],
            "data_devolucao_prevista": resultado[4],
            "data_devolucao": resultado[5]
        }

    def salvar(self, emprestimo):
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute(
            """INSERT INTO emprestimos
               (livro_isbn, leitor_cpf, data_emprestimo,
                data_devolucao_prevista)
               VALUES (?, ?, ?, ?)""",
            (
                emprestimo["livro_isbn"],
                emprestimo["leitor_cpf"],
                emprestimo["data_emprestimo"],
                emprestimo["data_devolucao_prevista"]
            )
        )

        conn.commit()

        id_emprestimo = cursor.lastrowid

        conn.close()

        return id_emprestimo


class ServicoNotificacao:
    def enviar(self, email, assunto, mensagem):
        try:
            msg = MIMEText(mensagem)

            msg["Subject"] = assunto
            msg["To"] = email

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()

            server.login(
                "biblioteca@exemplo.com",
                "senha"
            )

            server.send_message(msg)
            server.quit()

            return True

        except Exception:
            return False


class ServicoRelatorio:
    def gerar(self, emprestimo_id, livro, leitor, data_devolucao):
        nome_arquivo = f"comprovante_{emprestimo_id}.pdf"

        try:
            relatorio = canvas.Canvas(nome_arquivo)

            relatorio.drawString(
                100,
                750,
                f"Empréstimo #{emprestimo_id}"
            )

            relatorio.drawString(
                100,
                730,
                f"Livro: {livro['titulo']}"
            )

            relatorio.drawString(
                100,
                710,
                f"Leitor: {leitor['nome']}"
            )

            relatorio.drawString(
                100,
                690,
                f"Devolução: {data_devolucao}"
            )

            relatorio.save()

            return True

        except Exception:
            return False


class CalculadoraMulta:
    def calcular(self, data_devolucao_prevista):
        data_prevista = datetime.strptime(
            data_devolucao_prevista,
            "%Y-%m-%d"
        )

        if datetime.now() <= data_prevista:
            return 0

        dias_atraso = (
            datetime.now() - data_prevista
        ).days

        return dias_atraso * 2.0


class GerenciadorEmprestimo:
    def __init__(
        self,
        repo_livro,
        repo_leitor,
        repo_emprestimo,
        servico_notificacao,
        servico_relatorio,
        calculadora_multa
    ):
        self.repo_livro = repo_livro
        self.repo_leitor = repo_leitor
        self.repo_emprestimo = repo_emprestimo
        self.servico_notificacao = servico_notificacao
        self.servico_relatorio = servico_relatorio
        self.calculadora_multa = calculadora_multa

    def realizar_emprestimo(self, livro_isbn, leitor_cpf):
        livro = self.repo_livro.buscar(livro_isbn)

        if livro is None:
            return False, "Livro não encontrado."

        leitor = self.repo_leitor.buscar(leitor_cpf)

        if leitor is None:
            return False, "Leitor não encontrado."

        if livro["exemplares_disponiveis"] <= 0:
            return False, "Livro indisponível."

        data_emprestimo = datetime.now()

        data_devolucao = (
            data_emprestimo + timedelta(days=14)
        )

        emprestimo = {
            "livro_isbn": livro_isbn,
            "leitor_cpf": leitor_cpf,
            "data_emprestimo": data_emprestimo.strftime("%Y-%m-%d"),
            "data_devolucao_prevista":
                data_devolucao.strftime("%Y-%m-%d")
        }

        emprestimo_id = self.repo_emprestimo.salvar(
            emprestimo
        )

        livro["exemplares_disponiveis"] -= 1
        self.repo_livro.salvar(livro)

        self.servico_notificacao.enviar(
            leitor["email"],
            "Empréstimo Realizado",
            f"Empréstimo realizado: {livro['titulo']}"
        )

        self.servico_relatorio.gerar(
            emprestimo_id,
            livro,
            leitor,
            emprestimo["data_devolucao_prevista"]
        )

        return True, "Empréstimo realizado com sucesso."

    def calcular_multa(self, emprestimo_id):
        emprestimo = self.repo_emprestimo.buscar(
            emprestimo_id
        )

        if emprestimo is None:
            return 0

        return self.calculadora_multa.calcular(
            emprestimo["data_devolucao_prevista"]
        )


db_path = "biblioteca.db"

repo_livro = RepositorioLivro(db_path)
repo_leitor = RepositorioLeitor(db_path)
repo_emprestimo = RepositorioEmprestimo(db_path)

servico_notificacao = ServicoNotificacao()
servico_relatorio = ServicoRelatorio()
calculadora_multa = CalculadoraMulta()

gerenciador = GerenciadorEmprestimo(
    repo_livro,
    repo_leitor,
    repo_emprestimo,
    servico_notificacao,
    servico_relatorio,
    calculadora_multa
)
