package aula2.processoclinico;
import java.io.Serializable;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.List;
import java.util.Map;
import java.util.ArrayList;

public class EntradaAgenda implements Serializable {

    private LocalTime hora;
    private LocalDate data;
    private LocalTime duracao = LocalTime.parse("00:30:00");
    private Medico medico;
    private Utente utente;
    private String estado;

    public EntradaAgenda(LocalTime hora, LocalDate data, Medico medico, Utente utente, String estado) {
        this.hora = hora;
        this.data = data;
        this.medico = medico;
        this.utente = utente;
        this.estado = estado;
    }

    public LocalTime getHora() {
        return hora;
    }

    public void setHora(LocalTime hora) {
        this.hora = hora;
    }

    public LocalDate getData() {
        return data;
    }

    public void setData(LocalDate data) {
        this.data = data;
    }

    public LocalTime getDuracao() {
        return duracao;
    }



    public Medico getMedico() {
        return medico;
    }

    public void setMedico(Medico medico) {
        this.medico = medico;
    }

    public Utente getUtente() {
        return utente;
    }

    public void setUtente(Utente utente) {
        this.utente = utente;
    }

    public String getEstado() {
        return estado;
    }

    public void setEstado(String estado) {
        this.estado = estado;
    }

    @Override
    public String toString() {
        return "EntradaAgenda{" +
                "hora=" + hora +
                ", data=" + data +
                ", duracao=" + duracao +
                ", medico=" + medico +
                ", utente=" + utente +
                ", estado='" + estado + '\'' +
                '}';
    }

}
