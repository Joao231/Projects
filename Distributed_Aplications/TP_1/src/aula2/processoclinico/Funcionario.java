package aula2.processoclinico;

import java.io.Serializable;
import java.time.LocalDate;

public class Funcionario extends Pessoa implements Serializable {

    private int numfunc;

    public Funcionario(int numfunc) {
        this.numfunc = numfunc;
    }

    public Funcionario(String nome, String morada, String nif, String cc, LocalDate datanasc, int numfunc) {
        super(nome, morada, nif, cc, datanasc);
        this.numfunc = numfunc;
    }

    public int getNumfunc() {
        return numfunc;
    }

    public void setNumfunc(int numfunc) {
        this.numfunc = numfunc;
    }

    @Override
    public String toString() {
        return "Funcionario{" +
                super.toString()+
                "numfunc=" + numfunc +
                '}';
    }
}
