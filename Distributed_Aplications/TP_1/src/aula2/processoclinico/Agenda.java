package aula2.processoclinico;
import java.io.Serializable;
import java.util.Set;

import java.util.HashSet;

public class Agenda implements Serializable {

    private Set <EntradaAgenda> agenda;

    public Agenda(){
        agenda = new HashSet<>();
    }

    public Set<EntradaAgenda> getAgenda() {
        return agenda;
    }

    public void setAgenda(Set<EntradaAgenda> agenda) {
        this.agenda = agenda;
    }

    @Override
    public String toString() {
        return "Agenda{" +
                "agenda=" + agenda +
                '}';
    }
}
