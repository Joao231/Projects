package aula2.interfaces;

import java.io.IOException;
import java.rmi.Remote;
import java.rmi.RemoteException;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.*;

import aula2.exceptions.DoesNotExistsException;
import aula2.exceptions.MedicamentoNaoExisteException;
import aula2.exceptions.MedicoNaoExisteException;
import aula2.exceptions.UtenteNaoExisteException;
import aula2.processoclinico.Utente;
import aula2.progs.*;
import aula2.processoclinico.*;



public interface GestorInt extends Remote{

    public boolean LoginGestor(int numero, String passw ) throws RemoteException;

    public void AdicionaFunc(String nome, String morada, String nif, String cc, LocalDate datanasc, int numfunc) throws RemoteException;

    public void AdicionaMed(String nome, String morada, String nif, String cc, LocalDate datanasc, String cedula, String especialidade) throws RemoteException;

    public void AdicionaMec(String contador, String dci, String nome, String formafarmaceutica, String dosagem, String estadoautorizacao, boolean generico, String titular_aim) throws RemoteException;

    public void verlistaUtentes() throws RemoteException;

    public void verlistaMedicos() throws RemoteException;

    public void verlistaFuncionarios() throws RemoteException;

    public void utentes_idade(int ano) throws RemoteException;

    public void save_to(String file) throws IOException;

    public Set<EntradaAgenda> getAgenda() throws RemoteException;

    public Map<UUID, Consulta> getConsultas() throws RemoteException;

    public Map<String, Medico> getMedicos() throws RemoteException;

    public Map<String, Medicamento> getMedicamentos() throws RemoteException;

    public Map<Integer, Funcionario> getFuncionarios() throws RemoteException;

    public void criar_Observacoes(Consulta co, String observacoes) throws RemoteException;

    public Consulta adicionar_consulta(Medico med, String numutente, String Observacoes) throws RemoteException;

    public  void criar_prescricoes(Consulta co, String numutente,LocalDate data, Medicamento medc, String toma) throws RemoteException;
}
