package aula2.processoclinico;

import java.io.Serializable;

public class Medicamento implements Serializable {

    private String dci;
    private String nome;
    private String formafarmaceutica;
    private String dosagem;
    private String estadoautorizacao;
    private boolean generico;
    private String titular_aim;

    public Medicamento(String dci) {
        this.dci = dci;
    }

    public Medicamento(String dci, String nome, String formafarmaceutica, String dosagem, String estadoautorizacao, boolean generico, String titular_aim) {
        this.dci = dci;
        this.nome = nome;
        this.formafarmaceutica = formafarmaceutica;
        this.dosagem = dosagem;
        this.estadoautorizacao = estadoautorizacao;
        this.generico = generico;
        this.titular_aim = titular_aim;
    }

    public String getDci() {
        return dci;
    }

    public String getNome() {
        return nome;
    }

    public String getFormafarmaceutica() {
        return formafarmaceutica;
    }

    public String getDosagem() {
        return dosagem;
    }

    public String getEstadoautorizacao() {
        return estadoautorizacao;
    }

    public boolean isGenerico() {
        return generico;
    }

    public String getTitular_aim() {
        return titular_aim;
    }

    @Override
    public String toString() {
        return "Medicamento{" +
                "dci='" + dci + '\'' +
                ", nome='" + nome + '\'' +
                ", formafarmaceutica='" + formafarmaceutica + '\'' +
                ", dosagem='" + dosagem + '\'' +
                ", estadoautorizacao='" + estadoautorizacao + '\'' +
                ", generico=" + generico +
                ", titular_aim='" + titular_aim + '\'' +
                '}';
    }
}
