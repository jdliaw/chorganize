//
//  GroupFunctions.swift
//  ChOrganizeApp
//
//  Created by Hana on 12/12/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

func createGroup(email: String, groupName: String, completion: @escaping (_ success: Bool) -> Void) {
    //        /api/user/create
    print("in create group")
    
    let params = ["email": email,
                  "groupName": groupName]
    
    let url = URL(string: "http://shea3100.pythonanywhere.com/api/group/create")!
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
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
            print("error=\(error)")
            return
        }
        
        if let httpStatus = response as? HTTPURLResponse, httpStatus.statusCode != 200 {           // check for http errors
            print("statusCode should be 200, but is \(httpStatus.statusCode)")
            print("response = \(response)")
            // pop-up
        }
        
        // success, save user data / session
        let responseString = String(data: data, encoding: .utf8)
        print("responseString = \(responseString)")
        completion(true)
    }
    
    task.resume()
    print("end request")
}


func getGroups(email: String, completion: @escaping (_ groupslist: [Group]) -> Void){
    print("in get groups")
    var userGroups: [Group] = []
    
    var components = URLComponents(string: "http://shea3100.pythonanywhere.com/api/group/get-by-email")!
    components.queryItems = [URLQueryItem(name: "email", value: email)]
    var request = URLRequest(url: components.url!)
    request.httpMethod = "GET"
    
    let task = URLSession.shared.dataTask(with: request){ data, response, error in
        guard let data = data, error == nil else {
            print("error=\(error)")
            return
        }
        
        if let httpStatus = response as? HTTPURLResponse, httpStatus.statusCode != 200 {           // check for http errors
            print("statusCode should be 200, but is \(httpStatus.statusCode)")
            print("response = \(response)")
        }
        
        let responseString = String(data: data, encoding: .utf8)
        print("responseString = \(responseString)")
        
        do {
            let json = try JSONSerialization.jsonObject(with: data, options: .allowFragments) as! [String:Any]
            if let groupsItem = json["groups"] as? [[String: Any]] {
                for group in groupsItem {
                    if let name = group["name"] as? String {
                        if let id = group["id"] as? Int {
                            userGroups.append(Group(name: name, id: id)!)
                        }
                    }
                }
            }
            completion(userGroups)
        } catch let error as NSError {
            print(error)
        }
    }
    task.resume()
    print("end get groups")
    
    //return userGroups
}

func addUsersToGroup(groupID: Int, listOfEmails: [String], completion: @escaping (_ success: Bool) -> Void) {
    //        /api/user/create
    print("in add users to group")
    
    let params = ["groupID": groupID,
                  "listOfEmails": listOfEmails] as [String : Any]
    
    let url = URL(string: "http://shea3100.pythonanywhere.com/api/group/add-users")!
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
            print("error=\(error)")
            return
        }
        
        if let httpStatus = response as? HTTPURLResponse, httpStatus.statusCode != 200 {           // check for http errors
            print("statusCode should be 200, but is \(httpStatus.statusCode)")
            print("response = \(response)")
            // pop-up
        }
        
        // success, save user data / session
        let responseString = String(data: data, encoding: .utf8)
        print("responseString = \(responseString)")
        completion(true)
    }
    
    task.resume()
    print("end add users to group")
}

func removeUser(groupID: Int, email: String, completion: @escaping (_ success: Bool) -> Void) {
    //        /api/group/remove-user
    print("in remove user from group")
    
    let params = ["groupID": groupID,
                  "email": email] as [String : Any]
    
    let url = URL(string: "http://shea3100.pythonanywhere.com/api/group/remove-user")!
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
            print("error=\(error)")
            return
        }
        
        if let httpStatus = response as? HTTPURLResponse, httpStatus.statusCode != 200 {           // check for http errors
            print("statusCode should be 200, but is \(httpStatus.statusCode)")
            print("response = \(response)")
            // pop-up
        }
        
        // success, save user data / session
        let responseString = String(data: data, encoding: .utf8)
        print("responseString = \(responseString)")
        completion(true)
    }
    
    task.resume()
    print("end remove user from group")
}
