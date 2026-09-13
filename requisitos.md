Questão 1

Resposta da letra A:

Requisitos funcionais:

| ID  | Descrição | Prioridade |
| 001 | Os bibliotecários poderão cadastrar livros com título, autor, ISBN, categoria e quantidade de exemplares | Alta |
| 002 | Os leitores poderão se cadastrar com nome, CPF, email e telefone | Alta |
| 003 | O bibliotecário deverá registrar o empréstimo quando um leitor levar um livro | Alta |
| 004 | A data do empréstimo deverá ser registrada | Alta |
| 005 | A data prevista para devolução (de 14 dias) também deverá ser registrada | Alta |
| 006 | O leitor poderá reservar um livro quando todos os exemplares estiverem emprestados | Média |
| 007 | O primeiro leitor da fila será notificado quando um exemplar reservado for devolvido | Média |
| 008 | A renovação do empréstimo será permitida quando não houver reservas para o livro | Média |
| 009 | Deverá ser aplicada uma multa por devolução fora do prazo | Alta |
| 010 | A disponibilidade de exemplares precisa estar sempre atualizada | Alta |

Requisitos não funcionais:

| ID  | Categoria | Descrição | Métrica |
| 101 | Desempenho | Garantir resposta rápida nas consultas ao acervo | Até 2 segundos |
| 102 | Segurança | Armazenar senhas de forma protegida | Senhas armazenadas com hash |
| 103 | Usabilidade | Manter menus e botões de fácil compreensão | Feedback dos usuários |
| 104 | Recuperação de dados | Realizar cópias de segurança periódicas dos dados | Backup diário |
| 105 | Compatibilidade | Permitir acesso pelos principais navegadores | Chrome, Firefox e Edge |

Regras de negócio:

| ID  | Descrição |
| 201 | O prazo de devolução de um livro é de 14 dias |
| 202 | Quando todos os exemplares do livro estiverem emprestados, o leitor pode fazer uma reserva |
| 203 | Após a devolução do livro, o primeiro da fila de reservas será notificado por email |
| 204 | Para renovar o empréstimo, não pode haver reserva daquele livro |
| 205 | Quando atrasar, o leitor terá multa de R$ 2,00 por dia |

-------------------------------------------------------------------------------------------------------------------------

Resposta da letra B:

User story 1:

Como bibliotecário
Quero cadastrar um livro
Para deixá-lo disponível na biblioteca.

Critérios de Aceitação:

Deve conter título, autor, ISBN, categoria e quantidade de exemplares.
O livro deve ficar salvo no acervo.

Story Points: 3 

-------------------------------------------------------------------
User story 2:

Como leitor
Quero realizar meu cadastro
Para poder pegar livros emprestados.

Critérios de Aceitação:

Deve informar nome, CPF, email, telefone, endereço.
Seus dados precisam ficar salvos no sistema.

Story Points: 3

--------------------------------------------------------------------
User story 3:

Como bibliotecário
Quero registrar o empréstimo de um livro
Para manter o controle de entrada e saída de exemplares.

Critérios de Aceitação:

Vincular o empréstimo do livro a um leitor.
Registrar a data do empréstimo e a de devolução

Story Points: 5

--------------------------------------------------------------------
User story 4:

Como bibliotecário
Quero consultar a quantidade de exemplares disponíveis
Para verificar a possibilidade de empréstimo.

Critérios de Aceitação:

Exibir a quantidade total de exemplares cadastrados.
Exibir a quantidade disponível para empréstimo.

Story Points: 3

--------------------------------------------------------------------
User story 5:

Como leitor
Quero reservar um livro sem exemplares disponíveis
Para ter acesso ao livro quando for devolvido.

Critérios de Aceitação:

Permitir a reserva quando não houver exemplar disponível.
Inserir o leitor na fila.

Story Points: 5

---------------------------------------------------------------------
User story 6: 

Como leitor
Quero ser notificado quando um livro reservado for devolvido
Para poder realizar o empréstimo.

Critérios de Aceitação:

Identificar o primeiro leitor da fila.
Enviar uma notificação por email.

Story Points: 5
