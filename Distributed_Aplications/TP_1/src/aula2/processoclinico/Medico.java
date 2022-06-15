package aula2.processoclinico;

import java.io.Serializable;
import java.time.LocalDate;

public class Medico extends Pessoa implements Serializable {

    private String cedula;
    private String especialidade;

    public Medico(String cedula, String especialidade) {
        this.cedula = cedula;
        this.especialidade = especialidade;
    }

    public Medico(String nome, String morada, String nif, String cc, LocalDate datanasc, String cedula, String especialidade) {
        super(nome, morada, nif, cc, datanasc);
        this.cedula = cedula;
        this.especialidade = especialidade;
    }

    public String getCedula() {
        return cedula;
    }

    public void setCedula(String cedula) {
        this.cedula = cedula;
    }

    public String getEspecialidade() {
        return especialidade;
    }

    public void setEspecialidade(String especialidade) {
        this.especialidade = especialidade;
    }

    @Override
    public String toString() {
        return "Medico{" +
                super.toString() +
                "cedula='" + cedula + '\'' +
                ", especialidade='" + especialidade + '\'' +
                '}';
    }
}
