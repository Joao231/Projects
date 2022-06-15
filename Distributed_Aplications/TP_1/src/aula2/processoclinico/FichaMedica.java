package aula2.processoclinico;

import java.io.Serializable;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.chrono.ChronoLocalDateTime;
import java.util.*;
import java.util.stream.Collectors;

public class FichaMedica implements Serializable {



    private Utente utente;
    private List<Utente> agregado;
    private Map<LocalDate, Medicao> medicoes;
    private List<Prescricao> prescricoescronicas;
    private Map<LocalDate, Consulta> consultas;
    private String historico;

    public FichaMedica(Utente utente) {
        this.utente = utente;
        this.agregado = new ArrayList<>();
        this.medicoes = new TreeMap<>();
        this.prescricoescronicas = new ArrayList<>();
        this.consultas = new TreeMap<>();
    }

    public Utente getUtente(){
        return utente;
    }
    public String getHistorico() {
        return historico;
    }

    public void setHistorico(String historico) {
        this.historico = historico;
    }

    public void addConsulta(Consulta c){
        consultas.put(c.getData(), c);
    }
    public void addAgregado(Utente u){
        this.agregado.add(u);
    }

    public List<Utente> getAgregado(){
        return this.agregado;
    }
    public void addMedicao(Medicao medicao){
        this.medicoes.put(LocalDate.now(), medicao);
    }

    public Set<Medicao> medicoes(){
        return medicoes.values().stream().collect(Collectors.toSet());
    }

    public Set<Medicao> medicoes(LocalDate from, LocalDate to){
        return medicoes.keySet().stream()
                .filter(k-> k.isAfter(from) && k.isBefore(to))
                .map(k -> medicoes.get(k))
                .collect(Collectors.toSet());
    }

    public  Set<Medicao> medicoes2(LocalDate from, LocalDate to){
        Set<Medicao> res = new TreeSet<>();
        for(LocalDate t: medicoes.keySet()){
            if(t.isAfter(from) && t.isBefore(to)){
                res.add(medicoes.get(t));
            }

        }
        return res;
    }

    public Map<LocalDate, Consulta> getConsultas() {
        return consultas;
    }

    public void addPrescricaoCronica(Prescricao p){
        this.prescricoescronicas.add(p);
    }

    public List<Prescricao> getPrescricaoCronica(){
        return this.prescricoescronicas;
    }

    public void removePrescricaoCronica(Prescricao p){
        this.prescricoescronicas.remove(p);
    }

    @Override
    public String toString() {
        return "FichaMedica{" +
                "utente=" + utente +
                ", agregado=" + agregado +
                ", medicoes=" + medicoes +
                ", prescricoescronicas=" + prescricoescronicas +
                ", consultas=" + consultas +
                ", historico='" + historico + '\'' +
                '}';
    }


}

