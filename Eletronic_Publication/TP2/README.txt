# APLICAÇÃO-TP2
**Explicação do projeto prático 2 de Publicação Eletrónica**

A nossa aplicação foi feita com base no trabalho prático 1, onde todos os reports são de dois tipos,isto é, existem duas estruturas genéricas para os relatórios. Uma estrutura corresponde a ter um titulo, subtitulo, imagem de capa, autores, informaçao do curso, introducao, estrutura do tipo: questao e respetiva resposta e resolucao, referencias, um link para o relatorio em pdf e, por fim, uma descrição. A outra estrutura apresenta um titulo, subtitulo, imagem de capa, autores, informaçao do curso, texto com informacao relevante do assunto do relatorio, imagem final, conclusao, referencias, um link para o relatorio em pdf e, por fim, uma descrição. 

Para correr o nosso código é necessário, em primeiro lugar, correr o comando **"python3 ficheiro_auxiliar.py"**, de forma a povoar a nossa base de dados com 3 relatórios (provenientes da primeira parte). Para guardar informação de cada relatório foi criado um ficheiro shelve, designado por "relatorios.db", onde cada chave corresponde a relatório1, relatório2, etc... e sendo cada valor um dicionário onde está contida toda a informação do respetivo relatório. De seguida, correr o servidor (**"export FLASK_APP=TP2.py; export FLASK_ENV=development; flask run"**). Entrar em "http://127.0.0.1:5000/" para aceder à página inicial da nossa aplicação.

Nesta página inicial podemos aceder:

- Relatórios: onde podemos ver uma tabela com todos os relatórios existentes, e os respetivos tipos. Além disto, pode-se ver também uma barra de pesquisa, onde qualquer que seja a palavra pretendida a pesquisar, retornará o(s) relatório(s), e o(s) respetivo(s) lugar(es) onde essa mesma palavra aparece. Ao clicar em cada um dos relatórios, terá acesso a uma página com o conteúdo dos mesmos.

- Autores dos Relatórios: podemos ver uma lista com todos os autores que realizam os relatórios juntamente com os respetivos dados pessoais. Ao clicar em cada nome, irá redirecionar para a página que contém uma lista dos relatórios realizados por esse autor. Esses relatórios são, por sua vez, clicáveis para ver o seu conteudo.

- Description: podemos ver todas as tags, e os respetivos relatórios. Ao clicar em cada relatório, acede-se ao conteúdo do mesmo.

- Adicionar Relatórios: entra-se numa página onde podemos escolher o tipo de relatório (com a respetiva estrutura) a adicionar. 
Se selecionar o Tipo_1, os espaços de preenchimento obrigatório são: o subtítulo, nome_autor, numero_autor, introdução, referencias, link_ficheiro e descrição. Estes espaços estão assinalados com um *. Em cada espaço, caso precise de preencher com mais que um dado, separar por &. 
Ao preencher multiplos dados, por exemplo, colocar um número diferente de nome_autor em relação aos respetivos números ou emails ou telefone, não conseguirá submeter. Da mesma forma, se colocar múltiplos enunciados, a quantidade destes tem que ser igual à quantidade de respostas e explicações. 
Ao submeter com sucesso, o relatório é adicionado e pode-se voltar ao menu principal.
Se selecionar o Tipo_2, os espaços de preenchimento obrigatório são: o subtítulo, nome_autor, numero_autor, conclusão, referencias, link_ficheiro e descrição. Estes espaços estão assinalados com um *. Em cada espaço, caso precise de preencher com mais que um dado, separar por &. 
Ao preencher multiplos dados, por exemplo, colocar um número diferente de nome_autor em relação aos respetivos números ou emails ou telefone, não conseguirá submeter.
Ao submeter com sucesso, o relatório é adicionado e pode-se voltar ao menu principal.

- Update de Relatórios: aparece uma lista com todos os relatórios existentes e seleciona-se o relatório que se pretende alterar. Pode-se alterar qualquer espaço, tendo em atenção que os espaços de preenchimento obrigatório não podem ficar vazios. Fazendo submit, o relatório é alterado e pode voltar à página inicial.

- Remover Relatórios: aparece uma página onde apenas coloca o número do(s) relatório(s) que pretende eliminar (no caso de ser mais que um, separar por ","). Se o relatório que prentende eliminar não existir, aparece uma página de erro. Caso exista, o(s) relatório(s) selecionado(s), serão apagados.

- Autores do Projeto: contém os dados pessoais dos autores desta aplicação. 

Todo o código está comentado no ficheiro TP2.py, e na pasta templates encontram-se todos os templates usados na aplicação. 