//
//  ChoreFunction.swift
//  ChOrganizeApp
//
//  Created by Hana on 12/12/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

func createChore(name: String, groupID: Int, description: String = "", completion: @escaping (_ choreID: Int) -> Void) {
    //        /api/user/create
    print("in create chore")
    
    let params = ["name": name,
                  "groupID": groupID,
                  "description": description] as [String : Any]
    
    let url = URL(string: "http://shea3100.pythonanywhere.com/api/chore/create")!
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    
    do {
        request.httpBody = try JSONSerialization.data(withJSONObject: params, options: .prettyPrinted)
    } catch let error {
        print(error.localizedDescription)
    }
    print("successfully serialized body")
    request.addValue("application/json", forHTTPHeaderField: "Content-Type")
    request.addValue("application/json", forHTTPHeaderField: "Accept")
    
    let task = URLSession.shared.dataTask(with: request){ data, response, error in
        guard let data = data, error == nil else {
            print("error=\(String(describing: error))")
            return
        }
        
        if let httpStatus = response as? HTTPURLResponse, httpStatus.statusCode != 200 {           // check for http errors
            print("statusCode should be 200, but is \(httpStatus.statusCode)")
            print("response = \(String(describing: response))")
            // pop-up
        }
        
        // success, save user data / session
        if let responseString = String(data: data, encoding: .utf8) {
            print("responseString = \(String(describing: responseString))")
            completion(Int(responseString)!)
        }
    }
    
    task.resume()
    print("end request")
}

func getChores(email: String, groupID: Int, completed: String, completion: @escaping (_ choreslist: [Chore]) -> Void){
    print("in get chores")
    var userChores: [Chore] = []
    let strGroupID = String(groupID)
    
    var components = URLComponents(string: "http://shea3100.pythonanywhere.com/api/user/get-unfinished-chores")!
    components.queryItems = [URLQueryItem(name: "email", value: email), URLQueryItem(name: "groupID", value: strGroupID), URLQueryItem(name: "completed", value: completed)]
    var request = URLRequest(url: components.url!)
    print (request)
    request.httpMethod = "GET"
    
    let task = URLSession.shared.dataTask(with: request){ data, response, error in
        guard let data = data, error == nil else {
            print("error=\(String(describing: error))")
            return
        }
        
        if let httpStatus = response as? HTTPURLResponse, httpStatus.statusCode != 200 {           // check for http errors
            print("statusCode should be 200, but is \(httpStatus.statusCode)")
            print("response = \(String(describing: response))")
        }
        
        let responseString = String(data: data, encoding: .utf8)
        print("responseString = \(String(describing: responseString))")
        
        do {
            let json = try JSONSerialization.jsonObject(with: data, options: .allowFragments) as! [String:Any]
            if let choresList = json["Chorelist"] as? [[[String: Any]]] {
                if !choresList.isEmpty {
                    for choreItem in choresList {
                        for chore in choreItem {
                            if let name = chore["name"] as? String,
                                let date = chore["deadline"] as? String,
                                let id = chore["id"] as? Int,
                                let deadlinePassed = chore["deadlinePassed"] as? Bool,
                                let groupID = chore["groupID"] as? Int,
                                let userEmail = chore["userEmail"] as? String {
                                    let desc = chore["description"] as? String ?? ""
                                userChores.append(Chore(name: name, date: date, desc: desc, id: id, deadlinePassed: deadlinePassed, groupID: groupID, userEmail: userEmail)!)
                            }
                        }
                    }
                }
            }
            completion(userChores)
        } catch let error as NSError {
            print(error)
        }
    }
    task.resume()
    print("end get chores")
    
    //return userGroups
}

func assignUserToChore(id: Int, email: String, deadline: String, completion: @escaping (_ success: Bool) -> Void) {
    //        /api/group/remove-user
    print("in remove user from group")
    
    let params = ["id": id,
                  "email": email,
                  "deadline": deadline] as [String : Any]
    
    let url = URL(string: "http://shea3100.pythonanywhere.com/api/chore/assign")!
    var request = URLRequest(url: url)
    request.httpMethod = "PUT"
    print (request)
    
    do {
        request.httpBody = try JSONSerialization.data(withJSONObject: params, options: .prettyPrinted)
    } catch let error {
        print(error.localizedDescription)
    }
    print("successfully serialized body")
    request.addValue("application/json", forHTTPHeaderField: "Content-Type")
    request.addValue("application/json", forHTTPHeaderField: "Accept")
    
    let task = URLSession.shared.dataTask(with: request){ data, response, error in
        guard let data = data, error == nil else {
            print("error=\(String(describing: error))")
            return
        }
        
        if let httpStatus = response as? HTTPURLResponse, httpStatus.statusCode != 200 {           // check for http errors
            print("statusCode should be 200, but is \(httpStatus.statusCode)")
            print("response = \(String(describing: response))")
            // pop-up
        }
        
        // success, save user data / session
        let responseString = String(data: data, encoding: .utf8)
        print("responseString = \(String(describing: responseString))")
        completion(true)
    }
    
    task.resume()
    print("end remove user from group")
}

