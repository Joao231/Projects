package aula2.progs;

import aula2.exceptions.DoesNotExistsException;
import aula2.exceptions.MedicamentoNaoExisteException;
import aula2.exceptions.MedicoNaoExisteException;
import aula2.exceptions.UtenteNaoExisteException;
import aula2.processoclinico.*;
import aula2.interfaces.*;

import java.rmi.Remote;
import java.rmi.RemoteException;
import java.time.LocalTime;

import java.io.*;
import java.time.LocalDate;
import java.util.*;
import java.util.UUID;



public class PCmanager implements UtenteInt, GestorInt, MedicoInt, FuncionarioInt ,Serializable, Remote {


    private static final long serialVersionUID = -9149826635246618824L;
    private Map<String, FichaMedica> fichasUtente;
    private Map<String, Medico> medicos;
    private Map<Integer, Funcionario> funcionarios;
    private Map<String, Medicamento> medicamentos;
    public Map<Consulta, List<Exame> > exames = new HashMap<>();
    public Map<UUID, Consulta> consultas = new HashMap<>();
    public Set <EntradaAgenda> agenda = new HashSet<>();
    public Map<Integer, EntradaAgenda> eag =  new HashMap();
    private Map<String, Utente> utente_name;
    private Map<String, Utente> utente_nif;
    private Map<String, Utente> utente_nutente;
    private Map<String, Medico> medico_name;
    private Map<String, Medico> medico_nif;
    private Map<String, Medico> medico_cedula;
    private Map<String, Funcionario> funcionario_name;
    private Map<Integer, Funcionario> funcionario_numfunc;
    private Map<String, Funcionario> funcionario_nif;




    public PCmanager() {
        fichasUtente = new HashMap<>();
        medicos = new HashMap<>();
        funcionarios = new HashMap<>();
        medicamentos = new HashMap<>();
    }


    @Override
    public void save_to(String file) throws IOException {
        ObjectOutputStream os = new ObjectOutputStream( new FileOutputStream(file) );
        os.writeObject(this);
        os.close();
    }

    public static PCmanager load_from(String file) throws IOException, ClassNotFoundException {
        ObjectInputStream is = new ObjectInputStream( new FileInputStream(file));
        PCmanager o = (PCmanager) is.readObject();
        return o;
    }

    @Override
    public Map<String, FichaMedica> getFichasUtente() throws RemoteException{
        return fichasUtente;
    }


    @Override
    public Map<String, Medico> getMedicos() throws RemoteException{

        return medicos;
    }


    public Map<Integer, Funcionario> getFuncionarios() throws RemoteException{
        return funcionarios;
    }


    @Override
    public Map<String, Medicamento> getMedicamentos() throws RemoteException {
        return medicamentos;
    }

    @Override
    public Set<EntradaAgenda> getAgenda() throws RemoteException {
        return agenda;
    }


    public Map<UUID, Consulta> getConsultas() throws RemoteException{
        return consultas;
    }


    @Override
    public Utente getUtente(String nome) throws DoesNotExistsException {
        if (utente_name.containsKey(nome)) {
            return utente_name.get(nome);
        } else {
            throw new DoesNotExistsException();
        }
    }

    public Utente getUtente_nif(String nif) throws DoesNotExistsException {
        if (utente_nif.containsKey(nif)) {
            return utente_nif.get(nif);
        } else {
            throw new DoesNotExistsException();
        }
    }

    public Utente getUtente_numutente(String numutente) throws DoesNotExistsException {
        if (utente_nutente.containsKey(numutente)) {
            return utente_nutente.get(numutente);
        } else {
            throw new DoesNotExistsException();
        }
    }

    public Medico getMedico_name(String name) throws DoesNotExistsException {
        if (medico_name.containsKey(name)) {
            return medico_name.get(name);
        } else {
            throw new DoesNotExistsException();
        }
    }

    public Medico getMedico_nif(String nif) throws DoesNotExistsException {
        if (medico_nif.containsKey(nif)) {
            return medico_nif.get(nif);
        } else {
            throw new DoesNotExistsException();
        }
    }

    public Medico getMedico_cedula(String cedula) throws DoesNotExistsException {
        if (medico_cedula.containsKey(cedula)) {
            return medico_cedula.get(cedula);
        } else {
            throw new DoesNotExistsException();
        }
    }

    public Funcionario getFuncionario_name(String name) throws DoesNotExistsException {
        if (funcionario_name.containsKey(name)){
            return funcionario_name.get(name);
        } else {
            throw new DoesNotExistsException();
        }
    }
    public Funcionario getFuncionario_numfunc(String numfunc) throws DoesNotExistsException {
        if (funcionario_numfunc.containsKey(numfunc)) {
            return funcionario_numfunc.get(numfunc);
        } else {
            throw new DoesNotExistsException();
        }
    }
    public Funcionario getFuncionario_nif(String nif) throws DoesNotExistsException {
        if (funcionario_nif.containsKey(nif)) {
            return funcionario_nif.get(nif);
        } else {
            throw new DoesNotExistsException();
        }
    }



    public void AdicionarUtente(Utente t){
        this.fichasUtente.put(t.getNumutente(), new FichaMedica(t));
    }

    @Override
    public void AdicionaUtente(String Nome, String morada, String nif, String cc,
                               LocalDate dn, String nutente, String telefone,
                               String telefone_emergencia, String email) throws RemoteException{
        if (fichasUtente.containsKey(nutente)){
            System.out.println("Utente já existe");
        } else {
            Utente u = new Utente(Nome, morada, nif, cc, dn, nutente, telefone,
                    telefone_emergencia, email);
            AdicionarUtente(u);
        }
    }


    @Override
    public void AdicionaFunc(String nome, String morada, String nif, String cc, LocalDate datanasc, int numfunc) throws RemoteException{

        if (funcionarios.containsKey(numfunc)){
            System.out.println("Funcionario já existe");
        } else {
            Funcionario f = new Funcionario(nome, morada, nif, cc, datanasc, numfunc);
            AdicionarFunc(f);
        }
    }


    public void AdicionarFunc (Funcionario f){
        this.funcionarios.put(f.getNumfunc(), new Funcionario(f.getNome(),f.getMorada(),f.getNif(),f.getCc(),f.getDatanasc(),f.getNumfunc()));
    }

    @Override
    public void AdicionaMed(String nome, String morada, String nif, String cc, LocalDate datanasc, String cedula, String especialidade) throws RemoteException{
        if (medicos.containsKey(cedula)){
            System.out.println("Medico já existe");
        } else {
            Medico m = new Medico(nome, morada, nif, cc, datanasc, cedula, especialidade);
            AdicionarMed(m);
        }
    }

    public void AdicionarMed(Medico m){
        this.medicos.put(m.getCedula(), new Medico(m.getNome(),m.getMorada(),m.getNif(),m.getCc(),m.getDatanasc(),m.getCedula(), m.getEspecialidade()));
    }

    @Override
    public void AdicionaMec(String contador,String dci, String nome, String formafarmaceutica, String dosagem, String estadoautorizacao, boolean generico, String titular_aim) throws RemoteException{
        if (medicamentos.containsKey(contador)){
            System.out.println("Medicamento já existe");
        } else {
            Medicamento medc = new Medicamento(dci, nome, formafarmaceutica, dosagem, estadoautorizacao, generico, titular_aim);
            AdicionarMedc(medc, contador);
        }

    }

    public void AdicionarMedc(Medicamento medc,String contador){
        this.medicamentos.put(contador, new Medicamento(medc.getDci(), medc.getNome(), medc.getFormafarmaceutica(), medc.getDosagem(), medc.getEstadoautorizacao(),medc.isGenerico(), medc.getTitular_aim()));
    }

    @Override
    public synchronized boolean LoginGestor(int numero, String passw ) throws RemoteException{
        int numeroofic = 00200;
        String password = "alves.lda";
        boolean login = false;

        if (numero == numeroofic && passw.equals(password)){
            login = true;
            return true;
        }
        else{
            return false;
        }
    }



    @Override
    public synchronized String LoginUtente (String numutente, String nif) throws RemoteException {
        if (!this.fichasUtente.containsKey(numutente)) {
            System.out.println("Registe-se antes de fazer login.");
        } else if (!this.fichasUtente.get(numutente).getUtente().getNif().equals(nif)) {
            System.out.println("Password incorreta!");
        }
        else { return numutente; }
        return null;
    }


    @Override
    public synchronized String LoginMedico (String cedula, String nif) throws RemoteException {
        if (!this.medicos.containsKey(cedula)) {
            System.out.println("Registe-se antes de fazer login.");
        } else if (!this.medicos.get(cedula).getNif().equals(nif)) {
            System.out.println("Password incorreta!");
        }
        else { return cedula; }
        return null;
    }

    @Override
    public synchronized int LoginFunc (int numfunc, String nif) throws RemoteException {
        if (!this.funcionarios.containsKey(numfunc)) {
            System.out.println("Registe-se antes de fazer login.");
        } else if (! this.funcionarios.get(numfunc).getNif().equals(nif)) {
            System.out.println("Password incorreta!");
        }
        else { return numfunc; }
        return 0;
    }


    @Override
    public synchronized void marca_exame(UUID id_co,int idu, String tipo,
                                         String local, LocalDate data, LocalTime hora, LocalTime duracao_exame,
                                         double preco, boolean estado, ArrayList<String> observacoes)
            throws RemoteException {

        Exame ex;

        for (UUID id_consulta: consultas.keySet()){
            if (id_consulta.equals(id_co)){
                Consulta co = consultas.get(id_consulta);
                ex = new Exame(idu, tipo, local, data, hora, duracao_exame, preco, estado, observacoes);
                co.addExame(ex);
            }
        }
    }

    public synchronized Medico VerificarDisponiblidade(LocalDate data, LocalTime hora, String especialidade) throws RemoteException{
        for (Medico umedico: medicos.values()){
            if (umedico.getEspecialidade().equals(especialidade)){
                if (agenda.size() == 0){
                    return umedico;
                }
                else {
                    int contador=0;
                    for (EntradaAgenda eag : agenda) {
                        if (!umedico.equals(eag.getMedico())) {
                            contador += 1;
                        } else {
                            if (data.equals(eag.getData()) && hora.equals(eag.getHora())) {
                                break;
                            } else {
                                LocalTime t1 = eag.getHora().plusHours(eag.getDuracao().getHour());
                                LocalTime t2 = t1.plusMinutes(eag.getDuracao().getMinute());

                                if (hora.isBefore(t2)) {
                                    break;
                                } else {
                                    return umedico;
                                }
                            }
                        }
                    }
                    if (contador == agenda.size()){
                        return umedico;
                    }
                }

            }
        }

        return null ;
    }

    public synchronized Utente fornecer_utente(String numutente){
        Utente utente = null;
        for(String key : fichasUtente.keySet()){
            if (key.equals(numutente)){
                return fichasUtente.get(key).getUtente();
            }
        }
        return utente;
    }



    @Override
    public synchronized String marca_consulta(String numutente,LocalDate data, LocalTime hora, String especialidade)
            throws RemoteException, IOException {

        Medico medico = VerificarDisponiblidade(data, hora, especialidade);
        if (medico != null) {
            String estado = "Marcado";
            Utente utente = fornecer_utente(numutente);
            EntradaAgenda eag = new EntradaAgenda(hora, data, medico, utente, estado);
            agenda.add(eag);


        } else {
            return "Não é possivel marcar a consulta!";
        }

        return "Consulta marcada!";
    }


    @Override
    public synchronized void verlistaUtentes() throws RemoteException {
        for (FichaMedica fichamedica : fichasUtente.values()) {
            System.out.println(fichamedica.getUtente().getNome());
            utente_name.put(fichamedica.getUtente().getNome(), fichamedica.getUtente());
            utente_nif.put(fichamedica.getUtente().getNif(), fichamedica.getUtente());
            utente_nutente.put(fichamedica.getUtente().getNumutente(), fichamedica.getUtente());
        }

    }

    @Override
    public synchronized void verlistaMedicos() throws RemoteException {

        for (Medico umedico : medicos.values()) {
            //System.out.println(umedico);
            System.out.println(umedico.getNome());
            //medico_cedula.put(umedico.getCedula(), umedico);
            //medico_name.put(umedico.getNome(), umedico);
            //medico_nif.put(umedico.getNif(), umedico);
        }

    }

    @Override
    public synchronized void verlistaFuncionarios() throws RemoteException {
        for (Funcionario umfunc : funcionarios.values()) {
            System.out.println(umfunc.getNome());
            funcionario_nif.put(umfunc.getNif(), umfunc);
            funcionario_name.put(umfunc.getNome(), umfunc);
            funcionario_numfunc.put(umfunc.getNumfunc(), umfunc);

        }

    }



    public synchronized Medicao adicionar_medicao(LocalDate data, double peso, int altura, double glicemia, int tensaoarterial, int colesterol, int triglicerideos, int saturacao, int inr)
            throws RemoteException {

        Medicao medicao;

        medicao = new Medicao(data,peso, altura, glicemia, tensaoarterial,colesterol, triglicerideos, saturacao, inr);

        return medicao;
    }


    @Override
    public synchronized void criar_Observacoes(Consulta co, String observacoes) throws RemoteException{

        co.addObservacao(observacoes);

    }


    @Override
    public synchronized void adicionarObservacoes(UUID id_co,String observacoes) throws RemoteException{


        for (UUID id_consulta : consultas.keySet()) {

            if (id_consulta.equals(id_co)) {
                Consulta co = consultas.get(id_consulta);
                co.addObservacao(observacoes);
                System.out.println("Observacoes adicionadas!");
            }

        }
    }

    @Override
    public synchronized void adicionar_prescricoes(UUID id_co,LocalDate data, String toma, String dci, String nome, String formafarmaceutica, String dosagem, String estadoautorizacao, Boolean generico, String titular_aim) throws RemoteException{
        for (UUID id_consulta : consultas.keySet()) {
            if (id_consulta.equals(id_co)) {
                Consulta co = consultas.get(id_consulta);
                Medicamento medc = new Medicamento(dci, nome, formafarmaceutica, dosagem, estadoautorizacao, generico, titular_aim);

                Prescricao presc = new Prescricao(data, medc, toma);
                co.addPrescricao(presc);
                System.out.println("Prescricao adicionada!");


            }
        }
    }

    @Override
    public synchronized Consulta adicionar_consulta(Medico med, String numutente, String Observacoes) throws RemoteException {
        Consulta co = new Consulta(med);
        co.addObservacao(Observacoes);

        return co;
    }

    @Override
    public synchronized void criar_prescricoes(Consulta co, String numutente,LocalDate data, Medicamento medc, String toma) throws RemoteException {
        Prescricao p = new Prescricao(data, medc, toma);
        co.addPrescricao(p);
        for (String key : fichasUtente.keySet()){
            if (key.equals(numutente)){
                fichasUtente.get(key).addConsulta(co);
            }
        }
    }


    @Override
    public synchronized UUID realizarConsulta(String numu,LocalDate data,LocalTime hora, double peso, int altura, double glicemia, int tensaoarterial, int colesterol, int triglicerideos, int saturacao, int inr) throws RemoteException {

        UUID idco = UUID.randomUUID();
        String observacoes = "";
        List<Prescricao> prescricoes = new ArrayList<>();
        List<Exame> exames = new ArrayList<>();
        for (EntradaAgenda eag : agenda) {
            if (hora.equals(eag.getHora()) && data.equals(eag.getData()) && eag.getUtente().getNumutente().equals(numu)) {

                FichaMedica fu = fichasUtente.get(numu);
                Consulta c = new Consulta(eag.getData(), observacoes, prescricoes, exames);
                if (consultas.size() == 0){
                    c.setMedico(eag.getMedico());
                    fu.addConsulta(c);
                    Medicao medicao = adicionar_medicao(data, peso, altura, glicemia, tensaoarterial, colesterol, triglicerideos, saturacao, inr);
                    fu.addMedicao(medicao);
                    consultas.put(idco, c);
                    return idco;
                }
                else {
                    for (UUID key : consultas.keySet()) {
                        if (consultas.get(key).getData() == c.getData()) {
                            System.out.println("Consulta já realizada!");
                            System.out.println(key);
                            return key;
                        } else {
                            c.setMedico(eag.getMedico());
                            fu.addConsulta(c);
                            Medicao medicao = adicionar_medicao(data, peso, altura, glicemia, tensaoarterial, colesterol, triglicerideos, saturacao, inr);
                            fu.addMedicao(medicao);
                            consultas.put(idco, c);
                            return idco;
                        }
                    }
                }
            }
        }

        return null;
    }



    @Override
    public synchronized void adicionar_historico(String historico, String numutente) throws RemoteException{
        for(String numero : fichasUtente.keySet()){
            if (numero .equals (numutente)){
                FichaMedica fu = fichasUtente.get(numero);
                fu.setHistorico(historico);
            }
        }

    }

    @Override
    public synchronized void ver_fichaMedica(String numutente) throws RemoteException{
        for(String numero : fichasUtente.keySet()) {
            if (numero .equals (numutente)) {
                FichaMedica fu = fichasUtente.get(numero);
                System.out.println(fu);

            }
        }
    }

    @Override
    public synchronized void exames_utente(String numutente) throws RemoteException{

        for(String numero : fichasUtente.keySet()){
            if (numero .equals (numutente)){
                FichaMedica fu = fichasUtente.get(numero);

                for(Consulta co : fu.getConsultas().values()){
                    System.out.println(co.getExames());
                }
            }
        }
    }

    @Override
    public synchronized void consultas_utente(String numutente) throws RemoteException{

        for(String numero : fichasUtente.keySet()){
            if (numero .equals (numutente)){
                FichaMedica fu = fichasUtente.get(numero);
                System.out.println(fu.getConsultas());
            }
        }
    }


    @Override
    public synchronized void consultas_medico(String nummedico) throws RemoteException{

        for(Consulta co : consultas.values()){
            if (co.getMedico().getCedula().equals(nummedico)){
                System.out.println(co);
            }
        }
    }



    @Override
    public synchronized void utentes_idade(int ano) throws RemoteException{
        for (FichaMedica fic: fichasUtente.values()){
            Utente u = fic.getUtente();
            System.out.println(u.getNome());
           // if (u.getDatanasc().getYear() ==  ano){
                //System.out.println(u.getNome());
           // }
        }
    }

    @Override
    public synchronized int cancelar_consulta(String numutente, LocalDate data, LocalTime hora, String especialidade) throws RemoteException{
        for(EntradaAgenda eag : agenda ){

            if(numutente.equals(eag.getUtente().getNumutente()) && (data.equals(eag.getData())) && (hora.equals(eag.getHora())) && (especialidade.equals(eag.getMedico().getEspecialidade()))){
                agenda.remove(eag);
                System.out.println("Consulta cancelada!");
                return 1;

            }
        }
        return 0;

    }

}
