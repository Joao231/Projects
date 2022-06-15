package aula2.processoclinico;

import java.io.Serializable;
import java.time.LocalDate;

public class Prescricao implements Serializable {

    private LocalDate data;
    private Medicamento med;
    private String toma;

    public Prescricao() {
        data = LocalDate.now();
    }

    public Prescricao(LocalDate data, Medicamento med, String toma) {
        this.data = data;
        this.med = med;
        this.toma = toma;
    }

    public Medicamento getMed() {
        return med;
    }

    public void setMed(Medicamento med) {
        this.med = med;
    }

    public String getToma() {
        return toma;
    }

    public void setToma(String toma) {
        this.toma = toma;
    }

    @Override
    public String toString() {
        return "Prescricao{" +
                "data=" + data +
                ", med=" + med +
                ", toma='" + toma + '\'' +
                '}';
    }
}
