package aula2.interfaces;

import java.io.IOException;
import java.rmi.Remote;
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import aula2.exceptions.DoesNotExistsException;
import aula2.processoclinico.Utente;
import aula2.progs.*;
import aula2.processoclinico.*;



public interface FuncionarioInt extends Remote{

    public int LoginFunc (int numfunc, String nif) throws RemoteException;

    public void AdicionaUtente(String Nome, String morada, String nif, String cc,
                               LocalDate dn, String nutente, String telefone,
                               String telefone_emergencia, String email) throws RemoteException;

    public Utente getUtente(String nome) throws DoesNotExistsException, RemoteException;

    public void save_to(String file) throws IOException;










}
