package aula2.processoclinico;

import java.io.Serializable;
import java.time.LocalDate;

public class Medicao implements Serializable {

    private LocalDate data;
    private double peso;
    private int altura;
    private double glicemia;
    private int tensaoarterial;
    private int colesterol;
    private int triglicerideos;
    private int saturacao;
    private int inr;

    public Medicao() {
        data = LocalDate.now();
    }

    public Medicao(LocalDate data, double peso, int altura, double glicemia, int tensaoarterial, int colesterol, int triglicerideos, int saturacao, int inr) {
        this.data = data;
        this.peso = peso;
        this.altura = altura;
        this.glicemia = glicemia;
        this.tensaoarterial = tensaoarterial;
        this.colesterol = colesterol;
        this.triglicerideos = triglicerideos;
        this.saturacao = saturacao;
        this.inr = inr;
    }

    public double getPeso() {
        return peso;
    }

    public void setPeso(double peso) {
        this.peso = peso;
    }

    public int getAltura() {
        return altura;
    }

    public void setAltura(int altura) {
        this.altura = altura;
    }

    public double getGlicemia() {
        return glicemia;
    }

    public void setGlicemia(double glicemia) {
        this.glicemia = glicemia;
    }

    public int getTensaoarterial() {
        return tensaoarterial;
    }

    public void setTensaoarterial(int tensaoarterial) {
        this.tensaoarterial = tensaoarterial;
    }

    public int getColesterol() {
        return colesterol;
    }

    public void setColesterol(int colesterol) {
        this.colesterol = colesterol;
    }

    public int getTriglicerideos() {
        return triglicerideos;
    }

    public void setTriglicerideos(int triglicerideos) {
        this.triglicerideos = triglicerideos;
    }

    public int getSaturacao() {
        return saturacao;
    }

    public void setSaturacao(int saturacao) {
        this.saturacao = saturacao;
    }

    public int getInr() {
        return inr;
    }

    public void setInr(int inr) {
        this.inr = inr;
    }

    @Override
    public String toString() {
        return "Medicao{" +
                "data=" + data +
                ", peso=" + peso +
                ", altura=" + altura +
                ", glicemia=" + glicemia +
                ", tensaoarterial=" + tensaoarterial +
                ", colesterol=" + colesterol +
                ", triglicerideos=" + triglicerideos +
                ", saturacao=" + saturacao +
                ", inr=" + inr +
                '}';
    }
}
