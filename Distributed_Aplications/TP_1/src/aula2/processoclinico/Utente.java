package aula2.processoclinico;

import java.io.Serializable;
import java.time.LocalDate;

public class Utente extends Pessoa  implements Serializable {

    private String numutente;
    private String telefone;
    private String telefone_emergencia;
    private String email;

    public Utente(String numutente, String telefone, String telefone_emergencia, String email) {
        this.numutente = numutente;
        this.telefone = telefone;
        this.telefone_emergencia = telefone_emergencia;
        this.email = email;
    }

    public Utente(String nome, String morada,
                  String nif,
                  String cc, LocalDate datanasc,
                  String numutente, String telefone,
                  String telefone_emergencia, String email) {
        super(nome, morada, nif, cc, datanasc);
        this.numutente = numutente;
        this.telefone = telefone;
        this.telefone_emergencia = telefone_emergencia;
        this.email = email;
    }

    public String getNumutente() {
        return numutente;
    }

    public void setNumutente(String numutente) {
        this.numutente = numutente;
    }

    public String getTelefone() {
        return telefone;
    }

    public void setTelefone(String telefone) {
        this.telefone = telefone;
    }

    public String getTelefone_emergencia() {
        return telefone_emergencia;
    }

    public void setTelefone_emergencia(String telefone_emergencia) {
        this.telefone_emergencia = telefone_emergencia;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    @Override
    public String toString() {
        return "Utente{" +
                super.toString() +
                "numutente='" + numutente + '\'' +
                ", telefone='" + telefone + '\'' +
                ", telefone_emergencia='" + telefone_emergencia + '\'' +
                ", email='" + email + '\'' +
                '}';
    }
}
