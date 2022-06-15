package aula2.processoclinico;

import java.io.Serializable;
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.time.LocalDate;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.List;

public class Exame implements Serializable {

    private static int id_exame;
    public int idu;
    public String tipo;
    public String local;
    public LocalDate data;
    public LocalTime hora;
    public LocalTime duracao_exame;
    public double preco;
    public boolean estado;
    public List observacoes;


    public Exame(int idu, String tipo, String local, LocalDate data, LocalTime hora, LocalTime duracao_exame, double preco, boolean estado, ArrayList<String> observacoes) {
        this.idu = idu;
        this.tipo = tipo;
        this.local = local;
        this.data = data;
        this.hora = hora;
        this.duracao_exame = duracao_exame;
        this.preco = preco;
        this.estado = estado;
        this.observacoes = observacoes;

    }
    public Exame(int idu, String tipo, String local, LocalDate data, LocalTime hora) throws RemoteException {

        this.idu = idu;
        this.tipo = tipo;
        this.local = local;
        this.data=data;
        this.hora=hora;
    }

    public static int getId_exame() {
        return id_exame;
    }

    public static void setId_exame(int id_exame) {
        Exame.id_exame = id_exame;
    }

    public int getIdu() {
        return idu;
    }

    public void setIdu(int idu) {
        this.idu = idu;
    }

    public String getTipo() {
        return tipo;
    }

    public void setTipo(String tipo) {
        this.tipo = tipo;
    }

    public String getLocal() {
        return local;
    }

    public void setLocal(String local) {
        this.local = local;
    }

    public LocalDate getData() {
        return data;
    }

    public void setData(LocalDate data) {
        this.data = data;
    }

    public LocalTime getHora() {
        return hora;
    }

    public void setHora(LocalTime hora) {
        this.hora = hora;
    }

    public LocalTime getDuracao_exame() {
        return duracao_exame;
    }

    public void setDuracao_exame(LocalTime duracao_exame) {
        this.duracao_exame = duracao_exame;
    }

    public double getPreco() {
        return preco;
    }

    public void setPreco(double preco) {
        this.preco = preco;
    }

    public boolean isEstado() {
        return estado;
    }

    public void setEstado(boolean estado) {
        this.estado = estado;
    }

    public List getObservacoes() {
        return observacoes;
    }

    public void setObservacoes(List observacoes) {
        this.observacoes = observacoes;
    }



    @Override
    public String toString() {
        return "Exame{" +
                "idu=" + idu +
                ", tipo='" + tipo + '\'' +
                ", local='" + local + '\'' +
                ", data=" + data +
                ", hora=" + hora +
                ", duracao_exame=" + duracao_exame +
                ", preco=" + preco +
                ", estado=" + estado +
                ", observacoes=" + observacoes +
                '}';
    }
}
