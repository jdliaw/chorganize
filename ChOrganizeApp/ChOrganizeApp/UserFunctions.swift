//
//  UserFunctions.swift
//  ChOrganizeApp
//
//  Created by Hana on 12/12/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

func createUser(email: String, password: String, firstName: String, lastName: String = "", completion: @escaping (_ success: Bool) -> Void) {
    //        /api/user/create
    print("in create user")
    
    let params = ["email": email,
                  "password": password,
                  "firstName": firstName,
                  "lastName": lastName] as [String : Any]
    
    let url = URL(string: "http://shea3100.pythonanywhere.com/api/user/create")!
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
        let responseString = String(data: data, encoding: .utf8)
        print("responseString = \(String(describing: responseString))")
        completion(true)
    }
    
    task.resume()
    print("end create user")
}

func getUser(email: String, completion: @escaping (_ user: User) -> Void){
    print("in get user details")
    
    var components = URLComponents(string: "http://shea3100.pythonanywhere.com/api/user/get")!
    components.queryItems = [URLQueryItem(name: "email", value: email)]
    var request = URLRequest(url: components.url!)
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
//        print("responseString = \(String(describing: responseString))")
        
        do {
            let json = try JSONSerialization.jsonObject(with: data, options: .allowFragments) as! [String:Any]
            if let firstName = json["firstName"] as? String,
                let lastName = json["lastName"] as? String {
                    let user = User(firstName: firstName, lastName: lastName, email: email)!
                    completion(user)
            }
        } catch let error as NSError {
            print(error)
        }
    }
    task.resume()
    print("end get user details")
}

func getUserProgress(email: String, groupID: Int, completion: @escaping (_ progress: Int) -> Void) {
    print("getting user's progress for \(email) and group \(groupID)")
    
    var components = URLComponents(
        string: "http://shea3100.pythonanywhere.com/api/group/get-performance-by-group-and-email"
        )!
    components.queryItems = [URLQueryItem(name: "email", value: email), URLQueryItem(name: "groupID", value: String(groupID))]
    var request = URLRequest(url: components.url!)
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
            print("JSON")
            print(json["total"])
            if let total = json["total"] as? Int {
                print("retrieved progress: \(total)%")
                completion(total)
            }
        } catch let error as NSError {
            print(error)
        }
    }
    task.resume()
}

