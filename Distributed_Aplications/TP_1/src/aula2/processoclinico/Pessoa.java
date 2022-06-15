package aula2.processoclinico;

import java.io.Serializable;
import java.time.LocalDate;

public abstract class Pessoa implements Serializable {

    private String nome;
    private String morada;
    private String nif;
    private String cc;
    private LocalDate datanasc;

    public Pessoa() {
    }

    public Pessoa(String nome, String morada, String nif, String cc, LocalDate datanasc) {
        this.nome = nome;
        this.morada = morada;
        this.nif = nif;
        this.cc = cc;
        this.datanasc = datanasc;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getMorada() {
        return morada;
    }

    public void setMorada(String morada) {
        this.morada = morada;
    }

    public String getNif() {
        return nif;
    }

    public void setNif(String nif) {
        this.nif = nif;
    }

    public String getCc() {
        return cc;
    }

    public void setCc(String cc) {
        this.cc = cc;
    }

    public LocalDate getDatanasc() {
        return datanasc;
    }

    public void setDatanasc(LocalDate datanasc) {
        this.datanasc = datanasc;
    }

    @Override
    public String toString() {
        return "Pessoa{" +
                "nome='" + nome + '\'' +
                ", morada='" + morada + '\'' +
                ", nif='" + nif + '\'' +
                ", cc='" + cc + '\'' +
                ", datanasc=" + datanasc +
                '}';
    }
}
