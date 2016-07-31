#!/usr/bin/env python3
# Copyright (c) 2016 "Jonathan Yantis"
#
# This file is a part of MiniGraphDB.
#
#    This program is free software: you can redistribute it and/or  modify
#    it under the terms of the GNU Affero General Public License, version 3,
#    as published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    As a special exception, the copyright holders give permission to link the
#    code of portions of this program with the OpenSSL library under certain
#    conditions as described in each individual source file and distribute
#    linked combinations including the program with the OpenSSL library. You
#    must comply with the GNU Affero General Public License in all respects
#    for all of the code used other than as permitted herein. If you modify
#    file(s) with this exception, you may extend this exception to your
#    version of the file(s), but you are not obligated to do so. If you do not
#    wish to do so, delete this exception statement from your version. If you
#    delete this exception statement from all source files in the program,
#    then also delete it in the license file.
#
"""
MiniGraphDB Query Language

This code is an absolute mess, but is the start of a query language based on
Cypher for MiniGraphDB. This will likely require a major refactoring of the DB
itself to implement.
"""
from pyparsing import Word, Forward, Keyword, oneOf, alphas,\
    alphanums, nums, Optional, Group, quotedString, ParseException


def testGrammer(cyp):
    """ Test Parsing """
    print(cyp, "->")
    try:
        tokens = simpleCypher.parseString(cyp)
        print("tokens=", tokens)
        print("tokens.srcNode=", tokens.srcNode)
        print("tokens.firstTrOp=", tokens.firstTrOp)
        print("tokens.secondTrOp=", tokens.secondTrOp)
        print("tokens.dstNode=", tokens.dstNode)
        print("tokens.relVar=", tokens.relVar)
        print("tokens.relName=", tokens.relName)
        print("tokens.whereCond=", tokens.whereCond)
        print("tokens.return=", tokens.returnData)
    except ParseException as err:
        print(*err.loc + "\n" + err.msg)
        print(err)


matchStmt = Forward()
relExpr = Forward()
whereExpr = Forward()
matchToken = Keyword("match", caseless=True)
returnToken = Keyword("return", caseless=True)
pathToken = Keyword("path", caseless=True)
whereToken = Keyword("where", caseless=True)

ident = Word(alphas, alphanums).setName("identifier")
prop = Word(alphas, alphanums).setName("property")
binOp = oneOf("== != >= <= > < =~")
trOp = oneOf("- -> -> <- <-")
intNum = Word(nums)
whereVal = quotedString | intNum

whereCondition = Group((ident) + '.'
                       + prop + binOp
                       + whereVal)

whereExpr << whereToken + whereCondition.setResultsName("whereCond")

relExpr << '[' + Optional((ident).setResultsName("relVar")) + ':' + ident.setResultsName("relName") + ']'

matchStmt << (matchToken + '(' + (ident).setResultsName("srcNode") + ')' +
              Optional(trOp.setResultsName("firstTrOp") + Optional(relExpr) + trOp.setResultsName("secondTrOp")
              + '(' + ident.setResultsName("dstNode") + ')')
              + Optional(whereExpr)
              + returnToken + ((ident) + Optional('.' + prop)).setResultsName("returnData") )



simpleCypher = matchStmt

testGrammer('MATCH(A) RETURN A')
testGrammer('MATCH(A)-->(B) RETURN e')
testGrammer('MATCH(A)-[e1:E10G]->(B) RETURN e')
testGrammer('MATCH (A)-[e:TEST]->(B) WHERE A.type=="test" RETURN A.model')
