package com.zqzess;
/**
 * @Author zqzess
 * @Date 2022/5/22 13:37
 * @Project byyl
 * @Package com.zqzess
 * @Version 1.0
 * @Github https://github.com/zqzess
 * @Msg 亦余心之所善兮, 虽九死其尤未毁
 **/
import lombok.Data;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

// 二元式实体类
@Data
class TwoTuple {
    String type;
    String value;

    public TwoTuple(String type, String value) {
        this.type = type;
        this.value = value;
    }
}

// 标识符实体类
@Data
class Identify {
    String name;
    String type;
    String value;

    public Identify(String name, String type, String value) {
        this.name = name;
        this.type = type;
        this.value = value;
    }
}

// 四元式实体类
@Data
class FourTuple {
    String operator;
    String operand;
    String operand2;
    String result;

    public FourTuple(String operator, String operand, String operand2, String result) {
        this.operator = operator;
        this.operand = operand;
        this.operand2 = operand2;
        this.result = result;
    }
}

public class Main {

    static int index = 0;     // 读头
    static List<Identify> identifyTable = new ArrayList<>();    // 标识符列表
    static List<String> tempVar = new ArrayList<>();        // 临时变量列表
    static List<String> numberList = new ArrayList<>();     // 数字列表
    static List<String> identifyCheckList = new ArrayList<>();      // 标识符重复检查列表
    static List<FourTuple> middleTable = new ArrayList<>();     // 四元式列表
    static String codeStr = "";     // 源代码字符串
    static TwoTuple word;       // 二元式变量

    public static void main(String[] args) {
//        String path=this.getClass().getClassLoader().getResource("/");
        File file = new File("src/com/zqzess/in.txt");
        codeStr = readFromTXT(file);
        if (!codeStr.isEmpty()) {
            print(0, "代码块");
            print(2, "*****************");
            print(3, codeStr);
            print(2, "*****************");
            word = nextInput(); // 词法分析
            print(2, "[词]识别单词: " + word.toString());
            parseProgarm();     // 语法分析，语义分析入口
            // 打印标识符列表
            String tmp = "";
            for (Identify i : identifyTable) {
                tmp = tmp + i.getName() + "," + i.getType() + "," + i.getValue() + ";";
            }
            print(3, "identify table: " + tmp + "\n");
            // 打印数字列表
            tmp = "";
            for (String i : numberList) {
                tmp = tmp + i + ",";
            }
            tmp = tmp.substring(0, tmp.length() - 1);
            print(3, "const table: " + tmp + "\n");
            // 打印四元式
            tmp = "";
            int num = 0;
            String outData = "";
            for (FourTuple i : middleTable) {
                tmp = "(" + num + ") " + "(" + i.getOperator() + ", " + i.getOperand() + ", " + i.getOperand2() + ", " + i.getResult() + ")";
                num++;
                print(3, tmp);
                outData = outData + tmp + "\n";
            }
            // 四元式写入txt
            writeToTXT(outData);
        } else
            print(1, "输入的源代码为空");
    }


    // 从txt读取源代码
    public static String readFromTXT(File file) {
        Long filelength = file.length();
        byte[] filecontent = new byte[filelength.intValue()];
        try {
            FileInputStream in = new FileInputStream(file);
            in.read(filecontent);
            in.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
        String fileStr1 = new String(filecontent);
        return fileStr1;
    }

    // 将四元式写入txt
    static void writeToTXT(String data) {
        try {
            FileOutputStream fileOutputStream = null;
            File file = new File("src/com/zqzess/out.txt");
            if (!file.exists()) {
                file.createNewFile();
            }
            fileOutputStream = new FileOutputStream(file);
            fileOutputStream.write(data.getBytes(StandardCharsets.UTF_8));
            fileOutputStream.flush();
            fileOutputStream.close();
        } catch (Exception e) {
            e.printStackTrace();
            print(1, "\n写入错误");
        }
    }

    // 封装控制台输出
    static void print(String msg) {
        System.out.println(msg);
    }

    // 0 初始色彩，1 红色，2 绿色，3 黄色
    static void print(int color, String msg) {
        if (color == 0)
            System.out.println(msg);
        else if (color == 1)
            System.out.println("\033[31;1m" + msg + "\033[0m");
        else if (color == 2)
            System.out.println("\033[32;1m" + msg + "\033[0m");
        else if (color == 3)
            System.out.println("\033[33;1m" + msg + "\033[0m");
    }

    // 将标识符加入标识符列表
    static void addToIdentifyTable(String name, String type, String value) {
        boolean isExist = false;
        for (Identify t : identifyTable) {
            // 检查标识符是否已加入标识符列表
            if (t.getName().equals(name))
                isExist = true;
        }
        if (!isExist)
            identifyTable.add(new Identify(name, type, value));
    }

    // 临时变量列表
    static Identify tempVarTable() {
        String tmp = "";
        tempVar.add(tmp);
        int index2 = tempVar.size();
        String name = "T" + String.valueOf(index2);
        Identify identify = new Identify(name, "", "");
        return identify;
    }

    //通过name更新标识符列表type
    static void updateIdentifyTypeByName(String name, String type) {
        for (Identify t : identifyTable) {
            if (t.getName().equals(name)) {
                t.setType(type);
                break;
            }
        }
    }

    //通过name更新标识符列表value
    static void updateIdentifyValueByName(String name, String value) {
        for (Identify t : identifyTable) {
            if (t.getName().equals(name))
                t.setValue(value);
        }
    }

    // 通过name获取标识符value
    static String getIdentifyValueByName(String name) {
        for (Identify t : identifyTable) {
            if (t.getName().equals(name))
                return t.getValue();
        }
        return "";
    }

    // 加入四元式列表
    static void addToMiddleTable(String operator, String operand, String operand2, String result) {
        middleTable.add(new FourTuple(operator, operand, operand2, result));
    }

    // 返回四元式列表大小
    static int NXQ() {
        return middleTable.size();
    }

    // 回填
    static void backPath(int i, String result) {
        middleTable.get(i).setResult(result);
    }

    // 词法分析
    static TwoTuple nextInput() {
        int state = 1;
        String tmpStr = "";
        int count = codeStr.length();
        while (index <= count) {
            String i = "";
            char i2;
            try {
                i = String.valueOf(codeStr.charAt(index));
                i2 = codeStr.charAt(index);
            } catch (Exception e) {
                i = String.valueOf(codeStr.charAt(index - 1));
                i2 = codeStr.charAt(index - 1);
            }
//            String i = String.valueOf(codeStr.charAt(index));
//            char i2 = codeStr.charAt(index);
            if (!i.equals("#")) {
                if (i.equals(" ")) {
                    index++;
                    continue;
                }
                if (state == 1) {
                    tmpStr = "";
                    if (i.equals(";")) {
                        state = 4;
                        tmpStr += i;
                        index++;
                    }
                    if (i.equals(",")) {
                        state = 5;
                        tmpStr += i;
                        index++;
                    }
                    if (i.equals("=")) {
                        state = 6;
                        tmpStr += i;
                        index++;
                        continue;
                    }
                    if (i.equals("<")) {
                        state = 7;
                        tmpStr += i;
                        index++;
                        continue;
                    }
                    if (i.equals(">")) {
                        state = 8;
                        tmpStr += i;
                        index++;
                        continue;
                    }
                    if (i.equals("!")) {
                        state = 9;
                        tmpStr += i;
                        index++;
                        continue;
                    }
                    if (i.equals("+")) {
                        state = 11;
                        tmpStr += i;
                        index++;
                    }
                    if (i.equals("-")) {
                        state = 12;
                        tmpStr += i;
                        index++;
                    }
                    if (i.equals("*")) {
                        state = 13;
                        tmpStr += i;
                        index++;
                    }
                    if (i.equals("/")) {
                        state = 14;
                        tmpStr += i;
                        index++;
                    }
                    if (i.equals("(")) {
                        state = 15;
                        tmpStr += i;
                        index++;
                    }
                    if (i.equals(")")) {
                        state = 16;
                        tmpStr += i;
                        index++;
                    }
                    if (i.equals("i")) {
                        state = 21;
                        tmpStr += i;
                        index++;
                        continue;
                    }
                    if (i.equals("t")) {
                        state = 25;
                        tmpStr += i;
                        index++;
                        continue;
                    }
                    if (i.equals("e")) {
                        state = 29;
                        tmpStr += i;
                        index++;
                        continue;
                    }
                    if (i.equals("b")) {
                        state = 35;
                        tmpStr += i;
                        index++;
                        continue;
                    }
                    if (i.equals("w")) {
                        state = 40;
                        tmpStr += i;
                        index++;
                        continue;
                    }
                    if (i.equals("d")) {
                        state = 45;
                        tmpStr += i;
                        index++;
                        continue;
                    }
                    // 判断是否是数字
                    if (Character.isDigit(i2)) {
                        state = 47;
                        tmpStr += i;
                        index++;
                        continue;
                    }
                }
                if (state == 1 && i.equals("$")) {
                    state = 2;
                    tmpStr += i;
                    index++;
                    continue;
                }
                // 变量命名可以有英文可以有数字，不可以局限于纯英文
                if (state == 2) {
                    state = 3;
                    tmpStr += i;
                    index++;
                    continue;
                }
                if (state == 3) {
//                    if(Character.isLetter(i2))
//                    {
//                        // 判断是否为字母
//                        state = 3;
//                        tmpStr += i;
//                        index ++;
//                        continue;
//                    }
//                    else if(Character.isDigit(i2))
//                    {
//                        // 判读是否为数字
//                        state = 3;
//                        tmpStr += i;
//                        index ++;
//                        continue;
//                    }
                    if (Character.isLetterOrDigit(i2)) {
                        // 判断是否为字母或数字
                        state = 3;
                        tmpStr += i;
                        index++;
                        continue;
                    } else {
                        // 表示符
                        addToIdentifyTable(tmpStr, "", "");
                        return new TwoTuple("标识符", tmpStr);
                    }
                }// state == 3
                if (state == 4) {
                    // ;
                    return new TwoTuple("分号", tmpStr);
                }// state == 4
                if (state == 5) {
                    return new TwoTuple("逗号", tmpStr);
                }// state == 5
                if (state == 6) {
                    if (i.equals("=")) {
                        state = 6;
                        tmpStr += i;
                        index++;
                        continue;
                    } else {
                        if (tmpStr.length() == 1)
                            return new TwoTuple("赋值号", tmpStr);
                        else if (tmpStr.length() == 2)
                            return new TwoTuple("关系运算符", tmpStr);
                    }
                }// state == 6
                if (state == 7) {
                    // <
                    if (i.equals("=")) {
                        state = 7;
                        tmpStr += i;
                        index++;
                        continue;
                    } else
                        return new TwoTuple("关系运算符", tmpStr);
                }// state == 7
                if (state == 8) {
                    //>
                    if (i.equals("=")) {
                        state = 8;
                        tmpStr += i;
                        index++;
                        continue;
                    } else
                        return new TwoTuple("关系运算符", tmpStr);
                }// state == 8
                if (state == 9) {
                    // !
                    if (i.equals("=")) {
                        state = 9;
                        tmpStr += i;
                        index++;
                        continue;
                    } else
                        return new TwoTuple("关系运算符", tmpStr);
                }// state == 9
                if (state == 11)
                    return new TwoTuple("加法运算符", tmpStr);
                if (state == 12)
                    return new TwoTuple("减法运算符", tmpStr);
                if (state == 13)
                    return new TwoTuple("乘法运算符", tmpStr);
                if (state == 14)
                    return new TwoTuple("除法运算符", tmpStr);
                if (state == 15)
                    return new TwoTuple("左括号", tmpStr);
                if (state == 16)
                    return new TwoTuple("右括号", tmpStr);
                if (state == 21 && i.equals("n")) {
                    state = 22;
                    tmpStr += i;
                    index++;
                    continue;
                }
                if (state == 21 && i.equals("f")) {
                    state = 24;
                    tmpStr += i;
                }
                if (state == 22 && i.equals("t")) {
                    state = 23;
                    tmpStr += i;
                }
                if (state == 23) {
                    index++;
                    return new TwoTuple("int", tmpStr);
                }
                if (state == 24) {
                    index++;
                    return new TwoTuple("关键字if", tmpStr);
                }

                if (state == 25 && i.equals("h")) {
                    state = 26;
                    tmpStr += i;
                    index++;
                    continue;
                }
                if (state == 26 && i.equals("e")) {
                    state = 27;
                    tmpStr += i;
                    index++;
                    continue;
                }
                if (state == 27 && i.equals("n")) {
                    state = 28;
                    tmpStr += i;
                }
                if (state == 28) {
                    index++;
                    return new TwoTuple("关键字then", tmpStr);
                }

                if (state == 29 && i.equals("l")) {
                    state = 30;
                    tmpStr += i;
                    index++;
                    continue;
                }
                if (state == 29 && i.equals("n")) {
                    state = 33;
                    tmpStr += i;
                    index++;
                    continue;
                }
                if (state == 30 && i.equals("s")) {
                    state = 31;
                    tmpStr += i;
                    index++;
                    continue;
                }
                if (state == 31 && i.equals("e")) {
                    state = 32;
                    tmpStr += i;
                }
                if (state == 32) {
                    index++;
                    return new TwoTuple("关键字else", tmpStr);
                }


                if (state == 33 && i.equals("d")) {
                    state = 34;
                    tmpStr += i;
                }
                if (state == 34) {
                    index++;
                    return new TwoTuple("关键字end", tmpStr);
                }

                if (state == 35 && i.equals("e")) {
                    state = 36;
                    tmpStr += i;
                    index++;
                    continue;
                }
                if (state == 36 && i.equals("g")) {
                    state = 37;
                    tmpStr += i;
                    index++;
                    continue;
                }
                if (state == 37 && i.equals("i")) {
                    state = 38;
                    tmpStr += i;
                    index++;
                    continue;
                }
                if (state == 38 && i.equals("n")) {
                    state = 39;
                    tmpStr += i;
                }
                if (state == 39) {
                    index++;
                    return new TwoTuple("关键字begin", tmpStr);
                }
                if (state == 40 && i.equals("h")) {
                    state = 41;
                    tmpStr += i;
                    index++;
                    continue;
                }
                if (state == 41 && i.equals("i")) {
                    state = 42;
                    tmpStr += i;
                    index++;
                    continue;
                }
                if (state == 42 && i.equals("l")) {
                    state = 43;
                    tmpStr += i;
                    index++;
                    continue;
                }
                if (state == 43 && i.equals("e")) {
                    state = 44;
                    tmpStr += i;
                }
                if (state == 44) {
                    index++;
                    return new TwoTuple("关键字while", tmpStr);
                }


                if (state == 45 && i.equals("o")) {
                    state = 46;
                    tmpStr += i;
                }
                if (state == 46) {
                    index++;
                    return new TwoTuple("关键字do", tmpStr);
                }

                if (state == 47) {
                    if (Character.isDigit(i2)) {
                        state = 47;
                        tmpStr += i;
                        index++;
                        continue;
                    } else {
                        numberList.add(tmpStr);
                        return new TwoTuple("数字", tmpStr);
                    }
                }
                index++;
                tmpStr += i;
                return new TwoTuple("error", tmpStr);
            } // if(!i.equals("#"))
            else
                return new TwoTuple("#", "#");
        }
        return new TwoTuple(null, null);
    }

    // 匹配
    static boolean match(String type) {
        if (!type.equals(word.getType())) {
            print(3, "匹配失败: " + word.getValue());
            word = nextInput();
            print(2, "[词]识别单词: " + word.toString());
            return false;
        }
        word = nextInput();
        print(2, "[词]识别单词: " + word.toString());
        return true;
    }

    // 分析主程序
    static boolean parseProgarm() {
        print(0, "推导: <程序> →<变量说明部分>;<语句部分>");
        boolean T = parseExplainVars();
        if (!T)
            print(1, "语法错误：缺少变量申明");
        match("分号");
        parseStatementSection();
        return true;
    }

    static boolean parseExplainVars() {
        print(0, "推导: <变量说明部分> → int<标识符列表>");
        boolean T = match("int");
        if (!T)
            return false;
        else {
            parseIdentifierList("int");
            return true;
        }
    }

    static boolean parseIdentifierList(String type) {
        print(0, "推导: <标识符列表> → <标识符><标识符列表prime>");
        if (word.getType().equals("标识符")) {
            updateIdentifyTypeByName(word.getValue(), "int");
            print(0, "[翻]更新标识符" + word.getValue() + "为int");
            //  加入标识符重复检查列表
            identifyCheckList.add(word.getValue());
            match("标识符");
        } else
            print(1, "语法错误, 缺少标识符");
        parseIdentifierListPrime(type);
        return true;
    }

    static boolean parseIdentifierListPrime(String type) {
        print(0, "推导: <标识符列表prime> → ,<标识符><标识符列表prime>|ε");
        if (word.getType().equals("逗号")) {
            match("逗号");
            if (word.getType().equals("标识符")) {
                boolean isCheck = false;
                for (String i : identifyCheckList) {
                    if (word.getValue().equals(i)) {
                        print(1, "语义错误: 重复定义");
                        isCheck = true;
                    }
                }
                if (!isCheck)
                    identifyCheckList.add(word.getValue());
                updateIdentifyTypeByName(word.getValue(), "int");
                print(0, "[翻]更新标识符" + word.getValue() + "为int");
                match("标识符");
            } else {
                print(1, "语法错误： 缺少标识符");
//                print(1 , "语义错误： 标识符列表prime翻译失败");
            }
            parseIdentifierListPrime(type);
        }
        return true;
    }

    static boolean parseStatementSection() {
        print("推导: <语句部分> → <语句>;<语句部分prime>");
        parseStatement();
        match("分号");
        parseStatementSectionPrime();
        return true;
    }

    static boolean parseStatementSectionPrime() {
        if (word.getType().equals("标识符") || word.getType().equals("关键字if")) {
            print("推导: <语句部分prime> → <语句>;<语句部分prime>|ε");
            parseStatement();
            match("分号");
            parseStatementSectionPrime();
        } else if (word.getType().equals("标识符") || word.getType().equals("关键字while")) {
            print("推导: <语句部分prime> → <语句>;<语句部分prime>|ε");
            parseStatement();
            match("分号");
            parseStatementSectionPrime();
        }
        return true;
    }

    static boolean parseStatement() {
        if (word.getType().equals("标识符")) {
            print("推导: <语句> → <赋值语句>");
            parseAssignStatement();
        }
        if (word.getType().equals("关键字if")) {
            print("推导: <语句> → <条件语句>");
            parseIfStatement();
        }
        if (word.getType().equals("关键字while")) {
            print("推导: <语句> → <循环语句>");
            pareWhileStatement();
        }
        return true;
    }

    static boolean parseAssignStatement() {
        print("推导: <赋值语句> → <标识符>=<表达式>");
        String identifyname = "";
        if (word.getType().equals("标识符")) {
            identifyname = word.getValue();
            print("[翻]获取赋值语句标识符" + word.getValue());
            match("标识符");
        }
        boolean tmp = match("赋值号");
        Identify E = parseExpression();
        print("[翻]输出赋值语句四元式");
        addToMiddleTable("=", E.getName(), "null", identifyname);
        print("[翻]更新标识符" + identifyname + "值为" + E.getValue());
        updateIdentifyValueByName(identifyname, E.getValue());
        return true;
    }

    static boolean parseIfStatement() {
        print("推导: <条件语句> → if （<条件>） then <嵌套语句>; else <嵌套语句>");
        match("关键字if");
        match("左括号");
        Identify E = parseLogicExpression();
        match("右括号");
        match("关键字then");
        print("[翻]输出if语句真出口跳转四元式");
        addToMiddleTable("jnz", E.getName(), "null", String.valueOf(NXQ() + 2));
        int falseExit = NXQ();
        print("[翻]输出if语句假出口跳转四元式");
        addToMiddleTable("j", "null", "null", "0");
        int exitIndex = 0;
        if (word.getType().equals("关键字begin")) {
            print("推导: <嵌套语句> → <复合语句>");
            parseCounpoundStatement();
            exitIndex = NXQ();
            addToMiddleTable("j", "null", "null", "0");
            print("[翻]回填if语句假出口地址");
            backPath(falseExit, String.valueOf(NXQ()));
        } else {
            print("推导: <嵌套语句> → <语句>");
            parseStatement();
            exitIndex = NXQ();
            addToMiddleTable("j", "null", "null", "0");
            print("[翻]回填if语句假出口地址");
            backPath(falseExit, String.valueOf(NXQ()));
        }
        match("分号");
        match("关键字else");
        if (word.getType().equals("关键字begin")) {
            print("推导: <嵌套语句> → <复合语句>");
            parseCounpoundStatement();
            print("[翻]回填if语句出口地址");
            backPath(exitIndex, String.valueOf(NXQ()));
        } else {
            print("推导: <嵌套语句> → <语句>");
            parseStatement();
            print("[翻]回填if语句出口地址");
            backPath(exitIndex, String.valueOf(NXQ()));
        }
        return true;
    }

    static boolean pareWhileStatement() {
        print("推导: <循环语句> → while （<条件>） do <嵌套语句>");
        match("关键字while");
        match("左括号");
        int number = NXQ();
        Identify E = parseLogicExpression();
        match("右括号");
        match("关键字do");
        print("[翻]输出while语句真出口跳转四元式");
        addToMiddleTable("jnz", E.getName(), "null", String.valueOf(NXQ() + 2));
        int falseExit = NXQ();
        print("[翻]输出while语句假出口跳转四元式");
        addToMiddleTable("j", "null", "null", "0");
        int exitIndex = 0;
        if (word.getType().equals("关键字begin")) {
            print("推导: <嵌套语句> → <复合语句>");
            parseCounpoundStatement();
            exitIndex = NXQ();
            addToMiddleTable("j", "null", "null", "0");
            backPath(falseExit, String.valueOf(NXQ()));
        } else {
            print("推导: <嵌套语句> → <语句>");
            parseStatement();
            exitIndex = NXQ();
            addToMiddleTable("j", "null", "null", "0");
            backPath(falseExit, String.valueOf(NXQ()));
            print("[翻]回填while语句出口地址");
            backPath(exitIndex, String.valueOf(number));
        }
        return true;
    }

    static Identify parseExpression() {
        print("推导: <表达式> → <项><表达式prime>");
        Identify E = parseItem();
        Identify E2 = parseExpressionPrime(E);
        return E2;
    }

    static Identify parseExpressionPrime(Identify E) {
        if (word.getType().equals("加法运算符")) {
            print("推导: <表达式prime> → + <项><表达式prime>|ε");
            match("加法运算符");
            Identify E2 = parseItem();
            print("[翻]创建加法运算临时变量");
            Identify T = tempVarTable();
            print("[翻]输出加法运算四元式");
            addToMiddleTable("+", E.getName(), E2.getName(), T.getName());
            if (E.getValue().isEmpty())
                print(1, "语义错误: 未赋值");
            if ((!E.getValue().isEmpty()) && (!E2.getValue().isEmpty()))
                T.setValue(String.valueOf(Integer.parseInt(E.getValue()) + Integer.parseInt(E2.getValue())));
            else
//                print(1, "项计算失败");
                print(1, "表达式计算失败");
            Identify E3 = parseExpressionPrime(T);
            return E3;
        } else
            return E;
    }

    static Identify parseItem() {
        print("推导: <项> → <因子><项prime>|ε");
        Identify E = parseFactor();
        Identify E2 = parseItemPrime(E);
        if (!E2.getType().isEmpty())
            return E2;
        else
            return E;
    }

    static Identify parseItemPrime(Identify E) {
        if (word.getType().equals("乘法运算符")) {
            print("推导: <项prime> → <乘法运算符>");
            match("乘法运算符");
            Identify E2 = parseFactor();
            print("[翻]创建乘法运算临时变量");
            Identify T = tempVarTable();
            print("[翻]输出乘法四元式");
            addToMiddleTable("*", E.getName(), E2.getName(), T.getName());
            if ((!E.getValue().isEmpty()) && (!E2.getValue().isEmpty()))
                T.setValue(String.valueOf(Integer.parseInt(E.getValue()) + Integer.parseInt(E2.getValue())));
            else
                print(1, "语义错误：因子计算失败");
            Identify E3 = parseItemPrime(T);
            if (!E3.getValue().isEmpty())
                return E3;
            else
                return T;
        } else if (word.getType().equals("左括号")) {
            print("推导: <项prime> → <因子><项prime>");
            match("左括号");
            Identify E2 = parseFactor();
            Identify E3 = parseItemPrime(E2);
            return E3;
        } else
            return new Identify("", "", "");
    }

    static Identify parseFactor() {
        Identify E = new Identify("", "", "");
        if (word.getType().equals("标识符")) {
            print("推导: <因子> → <标识符>");
//            E = new Identify(word.getValue(),"","");
            E.setName(word.getValue());
            E.setValue(getIdentifyValueByName(word.getValue()));
            match("标识符");
        } else if (word.getType().equals("数字")) {
            print("推导: <因子> → <数字>");
//            E = new Identify(word.getValue(),"","");
            E.setName(word.getValue());
            E.setValue(word.getValue());
            match("数字");
        } else if (word.getType().equals("左括号")) {
            print("推导: <因子> → (<表达式>)");
            match("左括号");
            E = parseExpression();
            match("右括号");
        }
        return E;
    }

    static Identify parseLogicExpression() {
        print("推导: <条件> → <表达式><关系运算符><表达式>");
        Identify E = parseExpression();
        String logicOperator = word.getValue();
        boolean tmp = match("关系运算符");
        if (!tmp)
            print(1, "语法错误: 非关系运算符");
        Identify E2 = parseExpression();
        Identify T = tempVarTable();
        print("[翻]输出逻辑运算四元式");
        addToMiddleTable(logicOperator, E.getName(), E2.getName(), T.getName());
        T.setType("bool");
        String R1 = getIdentifyValueByName(E.getName());
        String R2 = getIdentifyValueByName(E2.getName());
        if (!R1.isEmpty() && !R2.isEmpty()) {
            int value1 = Integer.parseInt(R1);
            int value2 = Integer.parseInt(R2);
            if (logicOperator.equals("<")) {
                if (value1 < value2)
                    T.setValue("true");
                else
                    T.setValue("false");
            }
            if (logicOperator.equals(">")) {
                if (value1 > value2)
                    T.setValue("true");
                else
                    T.setValue("false");
            }
            if (logicOperator.equals("==")) {
                if (value1 == value2)
                    T.setValue("true");
                else
                    T.setValue("false");
            }
            if (logicOperator.equals("<=")) {
                if (value1 <= value2)
                    T.setValue("true");
                else
                    T.setValue("false");
            }
            if (logicOperator.equals(">=")) {
                if (value1 >= value2)
                    T.setValue("true");
                else
                    T.setValue("false");
            }
            if (logicOperator.equals("!=")) {
                if (value1 != value2)
                    T.setValue("true");
                else
                    T.setValue("false");
            }
            return T;
        }
        return T;
    }

    static boolean parseCounpoundStatement() {
        print("推导: <复合语句> → begin <语句部分> end");
        match("关键字begin");
        parseStatementSection();
        match("关键字end");
        return true;
    }
}
