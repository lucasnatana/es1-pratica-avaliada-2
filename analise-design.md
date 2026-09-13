Questão 3

Resposta da letra A:

O código viola os princípios SRP, OCP e DIP. Em relação ao SRP, a classe GerenciadorEmprestimo concentra várias responsabilidades, como acesso ao banco, cálculo de multa, envio de email e geração de PDF. Além disso, o OCP é violado porque qualquer mudança no tipo de notificação ou relatório exige alteração direta na classe. Já o DIP é prejudicado porque o gerenciador depende diretamente de tecnologias específicas, como SQLite, SMTP e ReportLab.

Ademais, em relação à coesão e ao acoplamento, a classe apresenta baixa coesão por reunir funções de naturezas diferentes e alto acoplamento por depender diretamente do banco de dados e de bibliotecas externas. 

Por fim, a principal refatoração é separar as responsabilidades em classes específicas, como repositórios para acesso aos dados, serviço de notificação, serviço de relatório e calculadora de multa.