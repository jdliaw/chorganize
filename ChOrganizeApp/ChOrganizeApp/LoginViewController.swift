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
    
    @IBOutlet weak var emailField: UITextField!
    @IBOutlet weak var passwordField: UITextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    private func moveToToDo() {
        print("in move to")
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let TabBarVC = storyboard.instantiateViewController(withIdentifier: "TabBarController") as! UITabBarController
        let appDelegate = UIApplication.shared.delegate as! AppDelegate
        appDelegate.window?.rootViewController = TabBarVC
    }
    
    private func emptyLoginParamsAlert() {
        let alert = UIAlertController(
            title: "Error",
            message: "Please enter a valid email and password to Login",
            preferredStyle: .alert)
        
        alert.addAction(UIAlertAction(title: NSLocalizedString("OK", comment: "Default action"), style: .`default`, handler: nil))
        self.present(alert, animated: true, completion: nil)
    }
    
    @IBAction func userLogin(_ sender: Any) {
        // TODO: validate fields
        // TODO: make password field starred out
        
        // check required fields are entered
        if emailField.text == "" || passwordField.text == "" {
            // popup alert
            emptyLoginParamsAlert()
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
        
        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: params, options: .prettyPrinted)
        } catch let error {
            print("Error serializing params for request")
            print(error.localizedDescription)
        }
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        request.addValue("appilcation/json", forHTTPHeaderField: "Accept")

        let task = URLSession.shared.dataTask(with: request){ data, response, error in
            guard let data = data, error == nil else {
                print("error=\(error)")
                return
            }
            
            if let httpStatus = response as? HTTPURLResponse, httpStatus.statusCode != 200 {
                print("statusCode should be 200, but is \(httpStatus.statusCode)")
                print("response = \(response)")
                // TODO: popup alert based on response
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
                        self.moveToToDo()
                    }
                }
            } catch let error as NSError {
                print(error)
                // TODO: login error popup (invalid credentials)
            }
        }
        task.resume()
    }
}
