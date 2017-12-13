//
//  LoginViewController.swift
//  ChOrganizeApp
//
//  Created by Hana on 11/8/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class LoginViewController: UIViewController {
    let BASE_URL = "http://shea3100.pythonanywhere.com"
    let VALIDATE_USER_URL = "/api/user/validate-password"
    let GET_USER_URL = "/api/user/get"
    
    @IBOutlet weak var emailField: UITextField!
    @IBOutlet weak var passwordField: UITextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    @IBAction func userLogin(_ sender: Any) {
        // TODO: validate fields
        
        // check required fields are entered
        if emailField.text == "" || passwordField.text == "" {
            loginErrorAlert(message: "Please enter a valid email and password to Login")
        }
        else {
            // try to validate user
            validateUserRequest()
        }
    }
    
    private func validateUserRequest() {
        let emailInput = emailField.text
        let passwordInput = passwordField.text
        
        // setup POST request for VALIDATE_USER_URL
        let url = URL(string: BASE_URL + VALIDATE_USER_URL)!
        let params = [
            "email": emailInput,
            "password": passwordInput
        ]
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        // serialize body for POST
        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: params, options: .prettyPrinted)
        } catch let error {
            print("Error serializing params for request")
            print(error.localizedDescription)
        }
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        request.addValue("appilcation/json", forHTTPHeaderField: "Accept")

        // perform request
        let task = URLSession.shared.dataTask(with: request){ data, response, error in
            guard let data = data, error == nil else {
                print("error=\(error)")
                return
            }
            if let httpStatus = response as? HTTPURLResponse, httpStatus.statusCode != 200 {
                print("statusCode should be 200, but is \(httpStatus.statusCode)")
                print("response = \(response)")
            }
            
            // request success
            let responseString = String(data: data, encoding: .utf8)
            print("responseString = \(responseString)")
            
            // parse response. only successful login if the result is true
            do {
                let json = try JSONSerialization.jsonObject(with: data, options: .allowFragments) as! [String: Any]
                let result = json["result"] as? Bool ?? nil
                
                // if result true, move to app homepage
                if result! {
                    DispatchQueue.main.async {
                        self.loginSuccessHandler(email: emailInput!)
                    }
                }
                else {
                    // login error popup (invalid credentials)
                    DispatchQueue.main.async {
                        self.loginErrorAlert(message: "Invalid email or password")
                    }
                }
            } catch let error as NSError {
                print(error)
            }
        }
        task.resume()
    }
    
    private func getUserRequest(email: String){// -> Dictionary<String, String> {
        // setup GET request for GET_USER_URL
        var components = URLComponents(string: BASE_URL + GET_USER_URL)!
        components.queryItems = [URLQueryItem(name: "email", value: email)]
        var request = URLRequest(url: components.url!)
        
        // perform request
        let task = URLSession.shared.dataTask(with: request){ data, response, error in
            guard let data = data, error == nil else {
                print("error=\(error)")
                return
            }
            if let httpStatus = response as? HTTPURLResponse, httpStatus.statusCode != 200 {
                print("statusCode should be 200, but is \(httpStatus.statusCode)")
                print("response = \(response)")
            }
            
            // request success
            let responseString = String(data: data, encoding: .utf8)
            print("responseString = \(responseString)")
            
            // parse response. only successful login if the result is true
            do {
                let json = try JSONSerialization.jsonObject(with: data, options: .allowFragments) as! [String: Any]
                let firstName = json["firstName"] as? String ?? nil
                let lastName = json["lastName"] as? String ?? nil
                let username = json["username"] as? String ?? nil
                print("returned object")
                print(firstName)
                
                let userInfo = [
                    "firstName": firstName,
                    "lastName": lastName,
                    "username": username
                ]
                //return userInfo // return user object
//                
//                DispatchQueue.main.async {
//                    let userInfo = [
//                        "firstName": firstName,
//                        "lastName": lastName,
//                        "username": username
//                    ]
//                    return userInfo // return user object
//                }
                
            } catch let error as NSError {
                print(error)
            }
        }
        task.resume()
    }
    
    private func loginSuccessHandler(email: String) {
        print("in handler")
        // TODO: use NSUSerDefaults to persist user email across app
        let defaults = UserDefaults.standard
        defaults.setValue(email, forKey: "email")
        
        let result = UserDefaults.standard.value(forKey: "email")
        print(result!)
      
        // Use NSUserDefaults to persist groups across app
        getGroups(email: email) {
            (groupslist: [Group]) in
            UserDefaults.standard.set(NSKeyedArchiver.archivedData(withRootObject: groupslist), forKey: "groups")
            
            if let data = UserDefaults.standard.object(forKey: "groups") as? NSData {
                let groups = NSKeyedUnarchiver.unarchiveObject(with: data as Data) as! [Group]
                print (groups)
            }
            
            OperationQueue.main.addOperation {
                self.moveToToDo()
            }
            
            // For each group get active and completed chores
//            let len = groupslist.count
//            let doublelen = len + len
//            let semaphore = DispatchSemaphore(value: doublelen)
//            
//            var chores = [[Chore]]()
//            
//            getChores(email: email, groupID: 1, completed: "true") {
//                (choreslist: [Chore]) in
//            }
//            for group in groupslist {
//                print (group.name)
//                // Get active chores
//                getChores(email: email, groupID: group.id, completed: "false") {
//                    (choreslist: [Chore]) in
//                    chores.append(choreslist)
//                    semaphore.signal()
//                }
//                // Get completed chores
//                getChores(email: email, groupID: group.id, completed: "true") {
//                    (choreslist: [Chore]) in
//                    chores.append(choreslist)
//                    semaphore.signal()
//                }
//            }

//            semaphore.wait(timeout: DispatchTime.distantFuture)
//            
//            defaults.set(NSKeyedArchiver.archivedData(withRootObject: chores), forKey: "activeChores")
//            defaults.set(NSKeyedArchiver.archivedData(withRootObject: chores), forKey: "completedChores")
//            
//            OperationQueue.main.addOperation {
//                self.moveToToDo()
//            }
        }
        
        // make request to get user's name (to show in settings)
       // var userInfo = getUserRequest(email: email)
//        defaults.setValue(userInfo["firstName"], forKey: "firstName")
//        if userInfo["lastName"] != nil {
//            defaults.setValue(userInfo["lastName"], forKey: "lastName")
//        }
//        if userInfo["username"] != nil {
//            defaults.setValue(userInfo["username"], forKey: "username")
//        }
//        
//        print("after get")
//        let name = UserDefaults.standard.value(forKey: "firstName")
//        print(name!)
//        
//        moveToToDo()
    }
    
    private func moveToToDo() {
        print("in move to")
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let TabBarVC = storyboard.instantiateViewController(withIdentifier: "TabBarController") as! UITabBarController
        let appDelegate = UIApplication.shared.delegate as! AppDelegate
        appDelegate.window?.rootViewController = TabBarVC
    }
    
    private func loginErrorAlert(message: String) {
        let alert = UIAlertController(
            title: "Error",
            message: message,
            preferredStyle: .alert)
        
        alert.addAction(UIAlertAction(title: NSLocalizedString("OK", comment: "Default action"), style: .`default`, handler: nil))
        self.present(alert, animated: true, completion: nil)
    }
}
