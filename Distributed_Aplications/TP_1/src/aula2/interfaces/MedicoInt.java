package aula2.interfaces;

import java.io.IOException;
import java.rmi.Remote;
import java.rmi.RemoteException;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import aula2.progs.*;
import aula2.processoclinico.*;

public interface MedicoInt extends Remote{

    public String LoginMedico(String cedula, String nif ) throws RemoteException;

    public void marca_exame(UUID id_co,int idu, String tipo,
                                         String local, LocalDate data, LocalTime hora, LocalTime duracao_exame,
                                         double preco, boolean estado, ArrayList<String> observacoes) throws RemoteException;

    public void adicionar_prescricoes(UUID id_co,LocalDate data, String toma,String dci, String nome, String formafarmaceutica, String dosagem, String estadoautorizacao, Boolean generico, String titular_aim) throws RemoteException;

    public void verlistaUtentes() throws RemoteException;

    public void adicionarObservacoes(UUID id_co,String observacoes)throws RemoteException;

    public UUID realizarConsulta(String numu, LocalDate data,LocalTime hora, double peso, int altura, double glicemia, int tensaoarterial, int colesterol, int triglicerideos, int saturacao, int inr) throws RemoteException;

    public void consultas_medico(String nummedico) throws RemoteException;

    public void adicionar_historico(String historico, String numutente) throws RemoteException;

    public void ver_fichaMedica(String numutente) throws RemoteException;

    public void exames_utente(String numutente) throws RemoteException;

    public void consultas_utente(String numutente) throws RemoteException;

    public Map<String, FichaMedica> getFichasUtente() throws RemoteException;

    public void save_to(String file) throws IOException;
}
