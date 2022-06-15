package aula2.processoclinico;

import java.io.Serializable;
import java.time.LocalDate;

import java.util.ArrayList;
import java.util.List;

public class Consulta implements Serializable {


    private LocalDate data;
    private String observacoes;
    private List<Prescricao> prescricoes;
    private List<Exame> exames;
    private Medico medico;

    public Consulta(LocalDate data) {
        this.data = data;
        this.observacoes="";
        this.prescricoes = new ArrayList<>();
        this.exames  = new ArrayList<>();
    }

    public Consulta(LocalDate data, String observacoes, List<Prescricao> prescricoes, List<Exame> exames) {
        this.data = data;
        this.observacoes = observacoes;
        this.prescricoes = prescricoes;
        this.exames = exames;
    }

    public Consulta() {
        this(LocalDate.now());
    }
    public Consulta(Medico m) {
        this(LocalDate.now());
        this.medico = m;
    }



    public void setMedico(Medico medico) {
        this.medico = medico;
    }


    public LocalDate getData() {
        return data;
    }

    public String getObservacoes() {
        return observacoes;
    }

    public List<Prescricao> getPrescricoes() {
        return prescricoes;
    }

    public List<Exame> getExames() {
        return exames;
    }
    public void addExame(Exame exame) {
        this.exames.add(exame);
    }

    public Medico getMedico() {
        return medico;
    }

    public void addObservacao(String obs){
        this.observacoes = this.observacoes.concat("\n"+obs);
    }

    public void addPrescricao(Prescricao p){
        this.prescricoes.add(p);
    }





    @Override
    public String toString() {
        return "Consulta{" +
                "data=" + data +
                ", observacoes='" + observacoes + '\'' +
                ", prescricoes=" + prescricoes +
                ", exames=" + exames +
                ", medico=" + medico +
                '}';
    }
}
